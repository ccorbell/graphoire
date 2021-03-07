#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 10:42:13 2021

@author: mathaes
"""

import numpy as np
from scipy.sparse import coo_matrix
import math

class Graph:
    """
    Graph is the set-theoretic graph class in graphworks.
    A graph is implemented here as a set of (implied) vertices and a 
    set of (explicit) edges that relate pairs of vertices by index reference.
    
    The class includes support for vertex and edge labels, 
    vertex and edge weights, and coloring. The Diagraph subclass
    adds support for edge direction.
    """
    
    def __init__(self, n):
        """
        Create an empty graph of size n.

        Parameters
        ----------
        n : integer
            Order (number of vertices) of the new graph.

        """
        self.n = n
        self.edges = []
        
        self.vtx_labels = None
        self.edge_labels = None
        
        self.vtx_weights = None
        self.edge_weights = None
        
        self.vtx_colors = None
        self.edge_colors = None
        
        self.directed = False
        
        self.degree_cache = {}
    
    def hasVertexLabels(self):
        return None != self.vtx_labels and len(self.vtx_labels) > 0
        
    def hasEdgeLabels(self):
        return None != self.edge_labels and len(self.edge_labels) > 0
	
    def hasVertexWeights(self):
        return None != self.vtx_weights and len(self.vtx_weights) > 0
	
    def hasEdgeWeights(self):
        return None != self.edge_weights and len(self.edge_weights) > 0
	
    def hasVertexColors(self):
        return None != self.vtx_colors and len(self.vtx_colors) > 0
	
    def hasEdgeColors(self):
        return None != self.edge_colors and len(self.edge_colors) > 0
	
    def order(self):
        return self.n
    
    def vertexDegree(self, v):
        """
        Return the degree of vertex v

        Parameters
        ----------
        v : int
            The zero-based vertex index.

        Raises
        ------
        Exception
            Throws exception for an out-of-range vertex index.

        Returns
        -------
        int
            The degree of vertex v (i.e. of undirected edges incident to v).
        """
        if v >= self.n:
            raise Exception(f"Vertex index {v} out of range for graph degree {self.n}")
        if v in self.degree_cache.keys():
            return self.degree_cache[v]
        
        degree = 0
        for edge in self.edges:
            if edge[0] == v or edge[1] == v:
                degree += 1
            if edge[0] > v:
                break

        self.degree_cache[v] = degree
        return degree
    
    def degreeMin(self):
        """
        Return the minimum vertex degree of the graph

        Returns
        -------
        degMin : int
            The minimum degree.
        """
        # TODO - cache degreeMin?
        if 0 == self.n:
            return None
        degMin = self.vertexDegree(0)
        for i in range(1, self.n):
            degMin = min(degMin, self.vertexDegree(i))
        return degMin                
        
    def degreeMax(self):
        """
        Return the maximum vertex degree of the graph.

        Returns
        -------
        degMax : int
            The maximum degree.
        """
        if 0 == self.n:
            return None
        degMax = self.vertexDegree(0)
        for i in range(1, self.n):
            degMax = max(degMax, self.vertexDegree(i))
        return degMax
    
    def degreeSum(self):
        """
        Return the total vertex-degree sum of the graph.

        Returns
        -------
        int
            The sum of all vertex degree

        """
        return len(self.edges) * 2
    
    def degreeAvg(self):
        if 0 == self.n:
            return None
        return float(self.degreeSum()) / float(self.n)
    
    def degreeSequence(self):
        seq = []
        for v in range(0, self.n):
            seq.append(self.vertexDegree(v))
        seq.sort()
        seq.reverse()
        return seq
    
    def hasEdge(self, i, j):
        v1 = i
        v2 = j
        if v1 > v2:
            v1 = j
            v2 = i
            
        if [v1, v2] in self.edges:
            return True
        return False
    
    def addEdge(self, i, j, sortEdges=False):
        # Note undirected graph always puts lowest vertex first;
        # GWDigraph overrides this to treat i as head, j as tail
        v1 = i
        v2 = j
        if v1 > v2:
            v1 = j
            v2 = i
        edge = [v1, v2]
        if not edge in self.edges:
            self.edges.append(edge)
        
        if True == sortEdges:
            self.sortEdges()
            
        self.clearCaches()
            
    def sortEdges(self):
        self.edges.sort()
        
    def deleteVertex(self, vertex):
        
        if vertex < 0 or vertex >= self.n:
            raise Exception("vertex {vertex} not in range [0,{self.n}]")
        
        # to delete a vertex we need to delete edges
        # which reference it, delete any labels,
        # and then also shift all vertex references
        # greater than its index down by one
        
        # delete referencing edges
        edgeIndices = []
        for ei in range(0, len(self.edges)):
            edge = self.edges[ei]
            if edge[0] == vertex or edge[1] == vertex:
                edgeIndices.append(ei)
        edgeIndices.reverse()
        for ei in edgeIndices:
            self.deleteEdgeByIndex(ei)
        
        # delete any vertex label, shift higher keys down by 1
        if len(self.vertex_labels) > 0:
            if vertex in self.vertex_labels:
                del self.vertex_labels[vertex]
            # also shift keys of vertex labels
            for vOld in range(vertex+1, self.n):
                if vOld in self.vertex_labels:
                    self.vertex_labels[vOld-1] = self.vertex_labels[vOld]
                    del self.vertex_labels[vOld]
        
        # now decrement any subsequent vertex references
        # in edges - also must decrement edge label keys
        for ei in range(0, len(self.edges)):
            edge = self.edges[ei].copy()
            
            edgeShifted = False
            if edge[0] > vertex:
                self.edges[ei][0] = edge[0] - 1
                edgeShifted = True
            if edge[1] > vertex:
                self.edges[ei][1] = edge[1] - 1
                edgeShifted = True
            if edgeShifted and len(self.edge_labels) > 0:
                oldKey = str(edge)
                if oldKey in self.edge_labels:
                    newKey = str(self.edges[ei])
                    self.edge_labels[newKey] = self.edge_labels[oldKey]
                    del self.edge_labels[oldKey]
        
        # decrement graph order
        self.n -= 1
        
        self.clearCaches()
        
    def deleteEdge(self, edge):
        ei = -1
        try:
            ei = self.edges.index(edge)
        except ValueError:
            print(f"WARNING: deleteEdge: graph does not contain {edge}")
        if ei < 0:
            return
        
        self.deleteEdgeByIndex(ei)
        
    def deleteEdgeByIndex(self, ei):
        if ei < 0 or ei >= len(self.edges):
            raise Exception(f"Invalid edge index: {ei}")
        
        edge = self.edges[ei]
        if str(edge) in self.edge_labels:
            del self.edge_labels[str(edge)]
        
        del self.edges[ei]
        
        self.clearCaches()
    
    def getEdgesForVertex(self, vertex):
        retEdges = []
        for edge in self.edges:
            if vertex in edge:
                retEdges.append(edge)
            elif edge[0] > vertex:
                break
        return retEdges
    
    def getNeighbors(self, vertex):
        neighbors = []
        for edge in self.edges:
            if edge[0] == vertex:
                neighbors.append(edge[1])
            elif edge[1] == vertex:
                neighbors.append(edge[0])
            elif edge[0] > vertex:
                # sorting means we won't find
                # any more neighbors
                break
        return neighbors
    
    def isEven(self):
        for v in range(0, self.n):
            deg = self.vertexDegree(v)
            if deg % 2 == 1:
                return False
        return True
        
    def isComplete(self):
        # fail fast: a complete graph needs n(n-1)/2
        numEdges = len(self.edges)
        if numEdges < self.n:
            return False
        expected = self.n * (self.n - 1) / 2
        if numEdges != expected:
            return False
        
        # For now we assume we don't have loops or
        # multiple edges, so we return true - may need
        # to refine later
        return True 
    
    
    
    def complement(self):
        comp = GWGraph(self.n)
        
        for i in range(0, self.n):
            for j in range(i+1, self.n):
                if i == j:
                    continue
                if not self.hasEdge(i, j):
                    comp.edges.append([i, j])
        return comp
    
    def inducedSubgraph(self, vertices):
        # Construct and return a GWGraph induced from a
        # set of vertices. If vertex and/or edge labels are
        # on the parent graph, they will be transferred to
        # the subgraph; vertex values themselves will not
        # be preserved, including within edges.
        #
        #  ... For example, vertices 1 and 3 in the parent graph
        # may become 0 and 1 in the induced subgraph; the
        # [1, 3] edge in the parent will be [0, 1] in the
        # induced subgraph. But if the parent graph labeled
        # vertex 1 as 'b' and vertex 3 as 'd', the subgraph
        # in this example will label its verex 0 as 'b' and
        # vertex 1 as 'd'.
        
        vertices.sort()
        
        inducedEdges = []
        
        for edge in self.edges:
            if edge[0] in vertices and edge[1] in vertices:
                if not edge in inducedEdges:
                    inducedEdges.append(edge)
 
        vtxMap = {}
        for vNew in range(0, len(vertices)):
            vtxMap[vertices[vNew]] = vNew
        
        sub = GWGraph(len(vertices))

        if len(self.vtx_labels) > 0:
            for vNew in range(0, len(vertices)):
                if vertices[vNew] in self.vtx_labels:
                    sub.vtx_labels[vNew] = self.vtx_labels[vertices[vNew]]

        for inducedEdge in inducedEdges:
            newEdge = [vtxMap[inducedEdge[0]], vtxMap[inducedEdge[1]]]
            
            if len(self.edge_labels) > 0:
                if str(inducedEdge) in self.edge_labels:
                    sub.edge_labels[str(newEdge)] = self.edge_labels[str(inducedEdge)]
                    
            sub.edges.append(newEdge)
            
        return sub
    
    def adjacencyMatrix(self):
        iList = []
        jList = []
        
        i = 0
        j = 0
        for i in range(0, self.n):
            for j in range(i+1, self.n):
                if self.hasEdge(i, j):
                    iList.append(i)
                    jList.append(j)
                    
                    iList.append(j)
                    jList.append(i)
        
        return coo_matrix((np.ones(len(iList), dtype=int), (iList, jList)), shape=(self.n, self.n))
        
    
    def edgeVertexMatrix(self):
        iList = []
        jList = []
        for i in range(0, len(self.edges)):
            edge = self.edges[i]
            iList.append(i)
            jList.append(edge[0])
            iList.append(i)
            jList.append(edge[1])
        return coo_matrix((np.ones(len(iList), dtype=int), (iList, jList)), shape=(len(self.edges), self.n))
        
    def incidenceMatrix(self):
        return self.edgeVertexMatrix().transpose()
    
    def clearCaches(self):
        self.degree_cache.clear()
        
    def __repr__(self):
        gwgstr = "GWGraph"
        gwgstr += "\n  n: " + str(self.n)
        gwgstr += "\n  edges: " + str(self.edges)
        if len(self.vtx_labels) > 0:
            gwgstr += "\n  vtx_labels: " + str(self.vtx_labels)
        if len(self.edge_labels) > 0:
            gwgstr += "\n  edge_labels: " + str(self.edge_labels)
        gwgstr += "\n"
        return gwgstr

    

    

    