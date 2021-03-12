#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 18:43:19 2021

@author: Christopher Corbell
"""


        
class Node:
    """
    Node represents a vertex in a linked-list graph implementation.
    This is an alternative to set-theoretic graph representation
    used by GWGraph, or its related matrix representations.
    
    Node is intended to be used for algorithms that are more
    efficient when traversing a graph as a linked list rather
    than treating the set of vertices/edges or a matrix representation.
    
    """
    def __init__(self, vtxref=None):
        self.vtxref = vtxref
        self.edges = []
        self.label = None
        self.weight = None
        
class Edge:
    """
    Edge represents an edge between two Node objects, for
    a linked-list graph implementation.
    
    If the graph is directed, then node0 is the tail
    and node1 is the head.
    """
    def __init__(self):
        self.node0 = None
        self.node1 = None
        self.label = None
        self.weight = None

class NodeGraph:
    """
    NodeGraph is a graph as a collection of linked nodes
    and edges.
    """
    def __init__(self):
        self.components = [] # list of disjoint Node graphs
    
    