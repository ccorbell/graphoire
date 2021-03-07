#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 18:43:19 2021

@author: Christopher Corbell
"""


        
class GWNode:
    """
    GWNode represents a vertex in a linked-list graph implementation.
    This is an alternative to set-theoretic graph representation
    used by GWGraph, or its related matrix representations.
    
    GWNode is intended to be used for algorithms that are more
    efficient when traversing a graph as a linked list rather
    than treating the set of vertices/edges or a matrix representation.
    """
    def __init__(self, vtxref=None):
        self.vtxref = vtxref
        self.edges = []
        self.label = None
        self.weight = None
        
class GWEdge:
    """
    GWEdge represents an edge between two GWNode objects, for
    a linked-list graph implementation.
    
    """
    def __init__(self):
        self.node0 = None
        self.node1 = None
        self.label = None
        self.weight = None

class GWNodeGraph:
    """
    GWNodeGraph is a graph as a collection of linked nodes
    and edges.
    """
    def __init__(self):
        self.components = [] # list of disjoint GWNode graphs
    
    