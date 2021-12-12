#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 10:42:13 2021

@author: Christopher Corbell
"""

import numpy as np
from scipy.sparse import coo_matrix

def vertexNeighborFromEdge(vertex, edge):
    if vertex == edge[0]:
        return edge[1]
    elif vertex == edge[1]:
        return edge[0]
    return None

class Graph:
    """
    Graph is the set-theoretic graph class in graphoire, and the primary
    graph class used for library facilities and algorithms. This base
    class is used to represent a simple undirected graph with no loops or
    multiple edges.
    
    The Graph class has an order, n, and an implied set of vertices
    corresponding to the integer set [n]. For programming convenience,
    these vertices are referred to by index (0 to n-1) rather than 1-based 
    ordinal value; i.e. vertices are elements of the set {n-1: n in [n]}.
    Edges are ordered pairs of vertex integer references.

    So for example the 4-vertex path P4 is represented by n = 4
    and the edges (0, 1), (1, 2), (2, 3).
    
    The Graph class supports optional dictionaries for vertex labels, weights,
    and colors, and the same for edges.
    
    In their set-theoretic form, as elements of [n]-1,
    indices are semantically arbitrary but always contiguous.
    
    A vspecific vertex deletion causes all vertices with higher indices to
    be decremented - this is reflected in references to those vertices
    in the edge set as well as in the optional label, weight, and/or
    color dictionaries.
    
    Internally an undirected graph always stores edges with lower-valued
    vertex index in the 0 or leftmost position of the pair. You can add
    an edge from 9 to 5, but it will be stored internall as (5, 9) in this
    class.
    
    The edge list should be kept sorted by calling sortEdges() after
    changes are made, for efficient lookup and use by algorithms. Several 
    Graph methods include a sortEdges parameter; providing True for this
    parameter will trigger a sortEdges() call after the method is applied.
    
    A directed graph is implemented by the subclass Digraph, which
    uses most of the base class facilities but permits both-direction
    edges. Direction in Digraph is defined by vertex-pair order, and so Digraph 
    does not force ascendant order of each edge pair's index values the way 
    this class does.
    
    Graphoire also supports two other graph representations: matrix
    representations (adjacency, incidence, Laplacian, etc.), and also
    tree-data-structure representation (with vertex objects linked by 
    edge objects). See graphoire.matrix and graphoire.nodegraph for these
    alternatives, and conversion between these types on this Graph class.
    
    For graph drawing, see graphoire.drawing.
    
    """
    
    def __init__(self, n: int):
        """
        Create an empty graph of order n.

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
        
        self.vertex_by_label_cache = None
        self.edge_by_label_cache = None
        
	
    
    def order(self):
        """
        Returns the order (number of vertices) of the graph.
        """
        return self.n
    
    def edgeCount(self):
        """
        Returns the size (number of edges) of the graph.
        """
        return len(self.edges)
    
    # ------------------------------ vertex degrees
    
    def vertexDegree(self, vertex):
        """
        Return the degree of vertex v

        Parameters
        ----------
        vertex : int
            The zero-based vertex index.

        Raises
        ------
        Exception
            Throws exception for an out-of-range vertex index.
        """
        if vertex < 0 or vertex >= self.n:
            raise Exception(f"Vertex index {vertex} out of range for graph degree {self.n}")
        if vertex in self.degree_cache.keys():
            return self.degree_cache[vertex]
        
        degree = 0
        for edge in self.edges:
            if edge[0] == vertex or edge[1] == vertex:
                degree += 1
            if edge[0] > vertex:
                break

        self.degree_cache[vertex] = degree
        return degree
    
    def degreeMin(self):
        """
        Return the minimum vertex degree of the graph
        """
        if 0 == self.n:
            return None
        degMin = self.vertexDegree(0)
        for i in range(1, self.n):
            degMin = min(degMin, self.vertexDegree(i))
        return degMin                
        
    def degreeMax(self):
        """
        Return the maximum vertex degree of the graph.
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
        """
        return len(self.edges) * 2
    
    def degreeAvg(self):
        """
        Return the average vertex degree, as a float
        """
        if 0 == self.n:
            return None
        return float(self.degreeSum()) / float(self.n)
    
    def degreeSequence(self):
        """
        Return the degree sequence of the graph, as a list of integers in decreasing magnitude.
        """
        seq = []
        for v in range(0, self.n):
            seq.append(self.vertexDegree(v))
        seq.sort()
        seq.reverse()
        return seq
    
    def hasEdge(self, v1, v2):
        """
        Returns True if this Graph has an edge between vertices v1 and v2.

        Parameters
        ----------
        v1 : int
            Index of vertex 1
        v2 : TYPE
            Index of vertex 2.
            
        Digraph note
        ------------
        In a regular Graph order does not matter; in a Digraph,
        this will only find an edge with v1 as head, v2 as tail
        """
        if self.canonicalizeEdge([v1, v2]) in self.edges:
            return True
        return False
    
    def canonicalizeEdge(self, edge):
        v1st = edge[0]
        v2nd = edge[1]
        
        if not self.directed:
            # undirected edge needs to be sorted
            if v1st > v2nd:
                v1st = edge[1]
                v2nd = edge[0]
        return [v1st, v2nd]
    
    def addEdge(self, v1, v2, sortEdges=False):
        """
        Add an edge from vertex v1 to vertex v2

        Parameters
        ----------
        v1 : int
            Index of first vertex
        v2 : int
            Index of second vertex
        sortEdges : bool, optional
            Whether to sort the edges after this add. The default is False.
            
        Behavior
        --------
        Adds the edge if it does not already exist. If the edge
        already exists this is a no-op. In the case of a Digraph,
        vertex order is significant, with v1 as head and v2 as tail.

        """
        if v1 < 0 or v1 >= self.n or v2 < 0 or v2 >= self.n:
            raise Exception("Vertex index out of range for addEdge()")
            
        # Note undirected graph always puts lowest vertex first;
        # GWDigraph overrides this to treat i as head, j as tail
        edge = self.canonicalizeEdge([v1, v2])
        if not edge in self.edges:
            self.edges.append(edge)
        
        if True == sortEdges:
            self.sortEdges()
            
        self.clearCaches()
            
    def sortEdges(self):
        """
        Sort the list of edges. This methdo should be called any time the 
        edge list is modified, before any calculations that rely on the edge 
        list.
        """
        self.edges.sort()
        
    def deleteVertex(self, vertex):
        """
        Delete the vertex at the indicated index.

        Parameters
        ----------
        vertex : int
            The index of the vertex to delete

        Behaviors
        ---------
        Decreases graph order by 1 and removes and edges or other structures 
        that were referencing vertex.
        
        Note that all index-based vertex references greater than the one 
        deleted will be decremented, e.g. if vertex is 5, then after deletion 
        the old vertex 6 will now be 5, old 7 will now be 6, etc.
        
        Raises
        ------
        Exception
            If vertex index is out of range.
        """
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
        if self.hasVertexLabels():
            if vertex in self.vtx_labels:
                del self.vtx_labels[vertex]
            # also shift keys of vertex labels
            for vOld in range(vertex+1, self.n):
                if vOld in self.vtx_labels:
                    self.vtx_labels[vOld-1] = self.vtx_labels[vOld]
                    del self.vtx_labels[vOld]
        
        # now decrement any subsequent vertex references
        # in edges - also must decrement edge label keys
        for ei in range(0, len(self.edges)):
            edge = self.edges[ei].copy() # review, is copy really needed?

            if edge[0] > vertex:
                self.edges[ei][0] = edge[0] - 1
            if edge[1] > vertex:
                self.edges[ei][1] = edge[1] - 1
                
        if self.hasEdgeLabels():
            newEdgeLabels = {}
            for key, value in self.edge_labels.items():
                key0 = key[0]
                key1 = key[1]
                if key0 >= vertex:
                    key0 -= 1
                if key1 >= vertex:
                    key1 -= 1
                newEdgeLabels[(key0, key1)] = value
            self.edge_labels = newEdgeLabels
        
        if self.hasEdgeWeights():
            newEdgeWeights = {}
            for key, value in self.edge_weights.items():
                key0 = key[0]
                key1 = key[1]
                if key0 >= vertex:
                    key0 -= 1
                if key1 >= vertex:
                    key1 -= 1
                newEdgeWeights[(key0, key1)] = value
            self.edge_weights = newEdgeWeights
        
        # decrement graph order
        self.n -= 1
        
        # Note there is no need to sort edges after a delete
        
        self.clearCaches()
        
    def deleteEdge(self, edge):
        """
        Delete an edge specified as vertex-index-list.

        Parameters
        ----------
        edge : list of two integers
            The two integers are the indices of the endpoint vertices.
        Raises
        ------
        Exception
            If Graph does not contain indicated edge.
        """
        
        edge = self.canonicalizeEdge(edge)
        ei = -1
        try:
            ei = self.edges.index(edge)
        except ValueError:
            print(f"WARNING: deleteEdge: graph does not contain {edge}")
        if ei < 0:
            return
        
        self.deleteEdgeByIndex(ei)
        
    def deleteEdgeByIndex(self, ei):
        """
        Delete edge by edge index.

        Parameters
        ----------
        ei : int
            The index of the edge to delete in the .edges list.

        Raises
        ------
        Exception
            If edge index is out of range.
        """
        if ei < 0 or ei >= len(self.edges):
            raise Exception(f"Invalid edge index: {ei}")
        
        edge = self.edges[ei]
        if None == edge:
            raise Exception(f"No edge found at index {ei}")
        
        if self.hasEdgeLabels():
            if (edge[0], edge[1]) in self.edge_labels:
                del self.edge_labels[(edge[0], edge[1])]
                
        if self.hasEdgeWeights():
            if (edge[0], edge[1]) in self.edge_weights:
                del self.edge_weights[(edge[0], edge[1])]
        
        del self.edges[ei]
        
        # Note there is no need to sort edges after a delete
        
        self.clearCaches()
    
    def getEdgesForVertex(self, vertex):
        """
        Get a list of edges for a vertex.

        Parameters
        ----------
        vertex : int
            The index of the vertex.

        Returns list of edges; each edge is a two-element vertex list [v1, v2]
        """
        retEdges = []
        for edge in self.edges:
            if vertex in edge:
                retEdges.append(edge)
            else:
                if not self.directed:
                    # optimization for sorted edges of undirected graphs -
                    # once we're past our vertex in edge-position 0 we're done
                    if edge[0] > vertex:
                        break
        return retEdges
    
    def getNeighbors(self, vertex):
        """
        Get a list of vertices adjacent to vertex.

        Parameters
        ----------
        vertex : int
            The vertex index

        Returns list of adjacent vertex integer indices.
        """
        neighbors = []
        for edge in self.edges:
            if edge[0] == vertex:
                neighbors.append(edge[1])
            elif edge[1] == vertex:
                neighbors.append(edge[0])
            else:
                if not self.directed:
                    if edge[0] > vertex:
                        # when undirected, sorting means we won't find
                        # any more neighbors
                        break
        return neighbors
    
    def isEven(self):
        """
        Returns True if all vertex degrees in Graph are even.
        """
        for v in range(0, self.n):
            deg = self.vertexDegree(v)
            if deg % 2 == 1:
                return False
        return True
        
    def isComplete(self):
        """
        Returns True if this is a complete graph (all vertices adjacent to 
        each other)
        """
        #  a complete graph needs n(n-1)/2
        numEdges = len(self.edges)
        expected = self.n * (self.n - 1) / 2
        if numEdges != expected:
            return False
        
        # For now we assume we don't have loops or
        # multiple edges, so we return true - may need
        # to refine later
        return True 
    
    def complement(self):
        """
        Returns a new Graph object that is the complement of the current
        graph, i.e., a graph of the same order with edges only between
        vertices that are not adjacent in the current graph.
        """
        comp = Graph(self.n)
        
        for i in range(0, self.n):
            for j in range(i+1, self.n):
                if i == j:
                    continue
                if not self.hasEdge(i, j):
                    comp.edges.append([i, j])
        return comp
    
    def inducedSubgraph(self, vertices):
        """
        Construct and return a new Graph that is isomorphic to the subgraph 
        induced on the list of vertices.

        Parameters
        ----------
        vertices : list of int
            The vertices used to induce the subgraph.
        
        Behavior
        --------
        Note that the returned graph will *not* have identical vertex-indices 
        to the original graph in most cases; vertex indicies are shifted to 
        reflect the order of the subgraph.
        
        For example if vertices 3, 4, 5 are supplied, the resulting graph 
        will have order 3 and vertex indicies 0, 1, 2, but the resulting 
        edges will be isomorphic (e.g. if original graph had an edge between 
        4 and 5, the induced subgraph will have an edge between 1 and 2).
        
        If the source graph is labeled, labels will be correctly assigned to 
        the induced subgraph (e.g. above if vertex 4 was labeled 'd', in the 
        induced subgraph the corresponding vertex 1 will be labeled 'd').
        
        Returns a new Graph object.
        """
        
        vertices.sort()
        
        inducedEdges = []
        
        for edge in self.edges:
            if edge[0] in vertices and edge[1] in vertices:
                if not edge in inducedEdges:
                    inducedEdges.append(edge)
 
        vtxMap = {}
        for vNew in range(0, len(vertices)):
            vtxMap[vertices[vNew]] = vNew
        
        sub = Graph(len(vertices))

        if self.hasVertexLabels():
            for vNew in range(0, len(vertices)):
                if vertices[vNew] in self.vtx_labels:
                    sub.vtx_labels[vNew] = self.vtx_labels[vertices[vNew]]

        for inducedEdge in inducedEdges:
            newEdge = [vtxMap[inducedEdge[0]], vtxMap[inducedEdge[1]]]
            
            if self.hasEdgeLabels():
                if (inducedEdge[0], inducedEdge[1]) in self.edge_labels:
                    sub.edge_labels[(newEdge[0], newEdge[1])] = self.edge_labels[(inducedEdge[0], inducedEdge[1])]
                    
            sub.edges.append(newEdge)
            
        return sub
    
    # ------------------------------ vertex labels
    
    def hasVertexLabels(self):
        """
        Returns true if this Graph object has any vertex labels set.
        """
        if None == self.vtx_labels:
            return False
        return len(self.vtx_labels) > 0
    
    def clearVertexLabels(self):
        """
        Delete any existing vertex labels.
        """
        if self.hasVertexLabels():
            del self.vtx_labels
            self.vtx_labels = None
            
    def setVertexLabel(self, vertex, label):
        if vertex < 0 or vertex >= self.n:
            raise Exception("vertex out of range")
            
        if None == self.vtx_labels:
            self.vtx_labels = {}
        self.vtx_labels[vertex] = label
        
    def getVertexLabel(self, vertex):
        if self.hasVertexLabels():
            return self.vtx_labels[vertex]
        return None
    
    def getVertexByLabel(self, label, useCache=True):
        if useCache:
            if None == self.vertex_by_label_cache:
                self.udpateVertexByLabelCache()
            if label in self.vertex_by_label_cache:
                return self.vertex_by_label_cache[label]
            return None
        else:
            for key, value in self.vtx_labels.items():
                if value == label:
                    return key
    
    def updateVertexByLabelCache(self):
        self.vertex_by_label_cache = dict([(value, key) for key, value in self.vtx_labels.items()])
        
    def clearVertexByLabelCache(self):
        del self.vertex_by_label_cache
        self.vertex_by_label_cache = None
        
    # ------------------------------ edge labels
    
    def hasEdgeLabels(self):
        """
        Returns true if this Graph object has any edge labels set.
        """
        return None != self.edge_labels and len(self.edge_labels) > 0
	
    def clearEdgeLabels(self):
        if self.hasEdgeLabels():
            del self.edge_labels
            self.edge_labels = None
            
    def setEdgeLabel(self, edge, label):
        edge = self.canonicalizeEdge(edge)
        if None == self.edge_labels:
            self.edge_labels = {}
        self.edge_labels[edge] = label
        
    def getEdgeLabel(self, edge):
        label = None
        if self.hasEdgeLabels():
            label = self.edge_labels.get(edge)
        return label
    
    def getEdgeByLabel(self, label, useCache=True):
        edge = None
        if useCache:
            if None == self.edge_by_label_cache:
                self.updateEdgeByLabelCache()
            edge = self.edge_by_label_cache.get(label)
        else:
            for key, value in self.edge_labels.items():
                if value == label:
                    edge = key
        return edge
        
    def updateEdgeByLabelCache(self):
        self.edge_by_label_cache = dict([(value, key) for key, value in self.vtx_labels.items()])
        
    def clearEdgeByLabelCache(self):
        del self.edge_by_label_cache
        self.edge_by_label_cache = None
    
    
    # ------------------------------ vertex weights
    
    def hasVertexWeights(self):
        """
        Returns true if this Graph object has any vertex weights set.
        """
        return None != self.vtx_weights and len(self.vtx_weights) > 0
    
    def setVertexWeight(self, vertex, weight):
        if None == self.vtx_weights:
            self.vtx_weights = {}
        self.vtx_weights[vertex] = weight
        
    def getVertexWeight(self, vertex):
        weight = None
        if self.hasVertexWeights():
            weight = self.vtx_weights.get(vertex)
        return weight
    
    
	
    # ------------------------------ edge weights
    
    def hasEdgeWeights(self):
        """
        Returns true if this Graph object has any edge weights set.
        """
        return None != self.edge_weights and len(self.edge_weights) > 0
    
    def setEdgeWeight(self, v1, v2, weight):
        if None == self.edge_weights:
            self.edge_weights = {}
        self.edge_weights[(v1, v2)] = weight
        
    def getEdgeWeight(self, v1, v2, default=None):
        if None == self.edge_weights:
            return default
        
        key = (v1, v2)
        if key in self.edge_weights:
            return self.edge_weights[key]
        
        return default
    
	
    # ------------------------------ vertex colors
    
    def hasVertexColors(self):
        """
        Returns true if this Graph object has any vertex colors set.
        """
        return None != self.vtx_colors and len(self.vtx_colors) > 0
    
    def getVertexColor(self, vertex):
        color = None
        if self.hasVertexColors():
            if vertex in self.vtx_colors.keys():
                color = self.vtx_colors.get(vertex)
        return color
    
    def setVertexColor(self, vertex, color):
        if None == self.vtx_colors:
            self.vtx_colors = {}
        self.vtx_colors[vertex] = color
        
    def hasCompleteVertexColoring(self):
        if not self.hasVertexColors():
            return False
        for vertex in range(0, self.n):
            if None == self.getVertexColor(vertex):
                return False
        return True
    
    def getVertexesByColor(self, color):
        results = []
        if self.hasVertexColors():
            for vertex in range(0, self.n):
                vcolor = self.getVertexColor(vertex)
                if vcolor == None:
                    if color == None:
                        results.append(vertex)
                elif (color != None) and (vcolor == color):
                    results.append(vertex)
        return results
	
    # ------------------------------ edge colors
    
    def hasEdgeColors(self):
        """
        Returns true if this Graph object has any edge colors set.
        """
        return None != self.edge_colors and len(self.edge_colors) > 0
    
    def getEdgeColor(self, edge):
        color = None
        if self.hasVertexColors():
            if vertex in self.vtx_colors.keys():
                color = self.vtx_colors.get(vertex)
        return color
    
    def setEdgeColor(self, edge, color):
        return
    
    def hasCompleteEdgeColoring(self):
        pass
    
    def getEdgesByColor(self, color):
        results = []
        
        return results
        
    
    # ------------------------------ misc.
    
    def clearCaches(self):
        """
        Clear internal caches. 
        
        Degree caches are used to avoid repeated calculation of vertex 
        degrees for a Graph that has not changed. Typically the caches are 
        cleared with any change to edge list, including vertex deletion etc.
        """
        self.degree_cache.clear()
        
    def __repr__(self):
        gstr = type(self).__name__
        if self.directed:
            gstr += "(directed)"
        else:
            gstr += "(undirected)"
        gstr += "\n  n: " + str(self.n)
        gstr += "\n  edges: " + str(self.edges)
        if self.hasVertexLabels():
            gstr += "\n  vtx_labels: " + str(self.vtx_labels)
        if self.hasEdgeLabels():
            gstr += "\n  edge_labels: " + str(self.edge_labels)
        if self.hasVertexWeights():
            gstr += "\n  vtx_weights: " + str(self.vtx_weights)
        if self.hasEdgeWeights():
            gstr += "\n  edge_weights: " + str(self.edge_weights)
        if self.hasVertexColors():
            gstr += "\n  vtx_colors: " + str(self.vtx_colors)
        if self.hasEdgeColors():
            gstr += "\n  edge_colors: " + str(self.edge_colors)
        return gstr

    

    

    