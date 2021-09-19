#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 10:10:02 2021

@author: mathaes
"""

from graphoire.graph import Graph

import math

class VertexCostHeap:
    def __init__(self):
        self.reset()
        
    def initialize(self, graph: Graph, s):
        self.reset()
        
        for n in range(0, graph.order()):
            self.insert(n, math.inf)
        
        self.decrease_key(s, 0)
        
    def insert(self, vertex, cost):
        self.vtx_costs[vertex] = cost
        
    def cost(self, vertex):
        return self.vtx_costs[vertex]
        
    def extract_min(self):
        if len(self.vtx_costs) == 0:
            return None
        
        keys = list(self.vtx_costs)
        
        min_value = self.vtx_costs[keys[0]]
        min_key = keys[0]
        
        for n in range(1, len(keys)):
            check_key = keys[n]
            check_value = self.vtx_costs[check_key]
            if check_value < min_value:
                min_value = check_value
                min_key = check_key
        
        return (min_key, self.vtx_costs.pop(min_key))
    
    def is_empty(self):
        return len(self.vtx_costs) == 0
    
    def decrease_key(self, vertex, cost):
        self.vtx_costs[vertex] = cost
        
    def reset(self):
        self.vtx_costs = {}
    
        
class Dijkstra:
    def __init__(self, graph: Graph):
        self.graph = graph
        self.source = 0
        self.warnings = []
        self.errors = []
        self.heap = {}
        self.costs = {} # summary of costs from source to each vertex
        self.parents = {} # for reconstructing lightest paths from source
        self.source = None
        self.heap = VertexCostHeap()
        
        if not self.graph.hasEdgeWeights():
            print("WARNING: graph for Dijkstra algorithm lacks edge weights, will treat each edge as cost=1")
            
    def reset(self, graph:Graph=None):
        self.graph = graph
        self.source = 0
        self.warnings = []
        self.errors = []
        self.heap = VertexCostHeap()
        self.costs = {}
        self.parents = {}
        self.source = None
        
    def findLeastCostPathImpl(self, s, t=None):
        self.source = s
        self.heap.initialize(self.graph, self.source)
        
        while not self.heap.is_empty():
            vtx, vtx_cost = self.heap.extract_min()
            self.costs[vtx] = vtx_cost
            
            if None != t and vtx == t:
                # this is all we need for this method
                return
            
            if self.heap.is_empty():
                break
            
            neighbors = self.graph.getNeighbors(vtx)
            for neighbor in neighbors:
                cur_cost = self.heap.cost(neighbor)
                edge_cost = self.graph.getEdgeWeight(vtx, neighbor)
                
                if cur_cost > vtx_cost + edge_cost:
                    neighbor_cost = vtx_cost + edge_cost
                    self.parents[neighbor] = vtx
                    self.heap.decrease_key(neighbor, neighbor_cost)
        
        
    def findLeastCostPath(self, s, t):
        """
        Find the least-cost path from s to t in terms of edge weights

        Parameters
        ----------
        s : the starting vertx.
        t : the ending vertex.

        Returns a path (list of vertices)
        
        Implementation: this uses the same algorithm as that which
        determines lest-cost paths to all vertices, it just stops when the
        target vertex shortest path is determined.

        """
        self.findLeastCostPathImpl(s, t)
        return self.getLeastCostPath(t)
    
    
    def findAllLeastCostPaths(self, s, t=None):
        """
        Calcualte the minimum-cost paths from s to all other vertices;
        return a dictionary of minimum costs from s

        Parameters
        ----------
        s : the starting vertex

        Returns
        -------
        A dictionary of vertex keys and total cost values.

        """
        self.findLeastCostPathImpl(s, None)
        return self.costs
        
    
    def getPathCost(self, t):
        """
        Get the total cost for the least-cost path from s to t;
        this is only valid after upstream call to findAllLeastCostPaths()
        (before any reset)

        Parameters
        ----------
        t : the target vertex that ends the path

        Returns
        -------
        The cost of the least-cost path from s to t

        """
        return self.costs[t]
    
    def getPath(self, t):
        """
        Get the least-cost path from s to t, as a list of vertices.

        Parameters
        ----------
        t : The target vertex

        Returns
        -------
        path : lix of vertex indexes, ordered from s to t

        """
        path = [t]
        v = self.parents[t]
        while None != v:
            path.append(v)
            if v == self.source:
                break
            
        path.reverse()
        return path
    
        
        