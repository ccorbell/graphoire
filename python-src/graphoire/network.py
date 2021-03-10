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
        
    def addNetworkEdge(self, tail: int, head: int, capacity: int):
        self.addEdge(tail, head)
        if None == self.edge_weights:
            self.edge_weights = {}
        self.edge_weights[str([tail, head])] = capacity
        
    def getEdgeCapacity(self, tail: int, head: int):
        key = str([tail, head])
        if key in self.edge_weights:
            return self.edge_weights[key]
        return None
    
    def setEdgeCapacity(self, tail: int, head: int, capacity: int):
        edge = [tail, head]
        if edge in self.edges:
            self.edge_weights[str(edge)] = capacity
            
    
    