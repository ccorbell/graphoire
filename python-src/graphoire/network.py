#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 22:24:43 2021

@author: mathaes
"""

from graphoire.digraph import Digraph

class Network(Digraph):
    """
    A network is a subclass of Digraph(Graph) that includes
    additional methods and accessors that relate to
    network graphs such as integer flow capacities, source and sink nodes,
    and some network-flow algorithms.
    """
    def __init__(self, n: int, source:int, sink:int):
        Digraph.__init__(self, n)
        self.source = source
        self.sink = sink
        self.edge_weights = {}
        
    def __repr__(self):
        nstr = Digraph.__repr__(self)
        nstr += f"\n.source: {self.source} .sink: {self.sink}"
        return nstr
        
    def addNetworkEdge(self, tail: int, head: int, capacity: int):
        self.addEdge(tail, head)
        self.setEdgeCapacity(tail, head, capacity)
        
    def getEdgeCapacity(self, tail: int, head: int):
        if not self.hasEdge(tail, head):
            return 0
        
        cap = self.getEdgeWeight(tail, head)
        if None == cap:
            cap = 0
        return cap
    
    def setEdgeCapacity(self, tail: int, head: int, capacity: int):
        self.setEdgeWeight(tail, head, capacity)
            
    def deleteVertex(self, vertex):
        
        if vertex == self.source or vertex == self.sink:
            raise Exception("Network object forbids deletion of source or sink vertex")
        
        # If vertex deleted has lower index then source and/or sink,
        # their values need to be shifted
        
        newSource = None
        newSink = None
        if vertex < self.source:
            newSource = self.source - 1
        if vertex < self.sink:
            newSink = self.sink - 1
            
        # Delete the vertex - this updates edges, weights, labels as well
        Digraph.deleteVertex(self, vertex)
        
        # Update source/sink index values if needed
        if None != newSource:
            self.source = newSource
        if None != newSink:
            self.sink = newSink
            
    