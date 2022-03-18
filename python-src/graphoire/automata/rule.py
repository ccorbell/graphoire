#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 14:44:35 2022

@author: mathaes
"""

from graphoire.graph import Graph


class Rule:
    """
    A Rule instance applies a particular type of transformation
    to a graph vertex based on neighboring vertices.
    
    Vertex weights are assumed to be used.
    
    Subclass this class to define specific rules. A sublcass should
    override determineVertexChange(), by storing the new weight for
    the vertex via
      self.vertexChanges[vertex] = (new value)
      
    This base class implementation simply copies current vertex weights if set.
    """
    def __init__(self):
        self.vertexChanges = {}
        pass
    
    def applyToGraph(self, graph: Graph):
        self.clear()
        for vertex in range(0, graph.order()):
            self.determineVertexChange(graph, vertex)
        self.applyChanges(graph)
        self.clear()
    
    def determineVertexChange(self, graph: Graph, vertex: int):
        # default simply stores current weight, if any
        vtxWeight = graph.getVertexWeight(vertex)
        if None != vtxWeight:
            self.vertexChanges[vertex] = vtxWeight
        pass
    
    def applyChanges(self, graph: Graph):
        #print(f"DBUG vertexChanges: {self.vertexChanges}")
        for change in self.vertexChanges.items():
            graph.setVertexWeight(change[0], change[1])
            
    def clear(self):
        self.vertexChanges.clear()

