#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 11:40:58 2021

@author: Christopher Corbell

Things we can use here:
    - construct Digraph from underlying Graph (default direction for edges)
    - DigraphFactory to construct some interesting digraphs
"""

from graphoire.graph import Graph

class Digraph(Graph):
    """
    Digraph is a subclass of Graph that implements edge direction.
    This includes distinguishing between u,v and v,u edges (the
    base class resolves such edges to u,v). The class also can
    calculate in-degree and out-degree of vertices; note that the
    base class vertexDegree() and related methods consider out-degree only.
    """
    
    def __init__(self, n: int):
        Graph.__init__(self, n)
        self.directed = True
        self.indegree_cache = {}
        
    def addEdge(self, i, j, sortEdges=False):
        # i = head, j = tail
        edge = [i, j]
        if not edge in self.edges:
            self.edges.append(edge)
        
        if True == sortEdges:
            self.sortEdges()
            
        self.degree_cache.clear()
        self.indegree_cache.clear()
        
    def vertexDegree(self, n):
        return self.vertexOutDegree(n)
    
    def vertexOutDegree(self, n):
        if n >= self.n:
            raise Exception(f"Vertex index {n} out of range for graph degree {self.n}")
        if n in self.degree_cache.keys():
            return self.degree_cache[n]
        
        degree = 0
        for edge in self.edges:
            if edge[0] == n:
                degree += 1
            if edge[0] > n:
                break

        self.degree_cache[n] = degree
        return degree
    
    def vertexInDegree(self, n):
        if n >= self.n:
            raise Exception(f"Vertex index {n} out of range for graph degree {self.n}")
            
        if n in self.indegree_cache.keys():
            return self.indegree_cache[n]
        
        degree = 0
        for edge in self.edges:
            if edge[1] == n:
                degree += 1

        self.indegree_cache[n] = degree
        return degree
    
    def getUnderlyingGraph(self):
        underG = Graph(self.n)
        # Add our directed edges to the undirected copy,
        # which will automatically consolidate any
        # duplicates and discard direction information
        for edge in self.edges:
            underG.addEdge(edge[0], edge[1])
        # Copy vertex labels but not edge labels
        if self.hasVertexLabels():
	        underG.vtx_labels = self.vtx_labels.copy()
        return underG
    
    def getOutNeighbors(self, vertex):
        """
        Get a list of vertices that this vertex connects-outward to.

        Parameters
        ----------
        vertex : int
            The vertex index

        Returns list of adjacent head-vertex integer indices.
        """
        neighbors = []
        for edge in self.edges:
            if edge[0] == vertex:
                neighbors.append(edge[1])
        return neighbors
    
    def getInNeighbors(self, vertex):
        """
        Get a list of vertices that connect inward to this vertex.

        Parameters
        ----------
        vertex : int
            The vertex index

        Returns list of adjacent tail-vertex integer indicdes.
        """
        neighbors = []
        for edge in self.edges:
            if edge[1] == vertex:
                neighbors.append(edge[0])
        return neighbors

    def edgeDirection(self, tail, head):
        """
        Get the direction of edge between tail and head.

        Parameters
        ----------
        tail : integer (vertex index)
            The vertex to interpret as tail
        head : integer (vertex index)
            The vertex to interpret as head

        Returns
        -------
        An integer value 1 if this is a directed edge from
        tail to head, -1 if the edge is the other direction,
        and 0 if there is no edge.
        """
        if self.hasEdge(tail, head):
            return 1
        elif self.hasEdge(head, tail):
            return -1
        else:
            return 0
        
    def clearCaches(self):
        self.indegree_cache.clear()
        Graph.clearCaches(self)
