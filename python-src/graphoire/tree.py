#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 11:21:49 2021

@author: Christopher Corbell
"""


from graphoire.graph import Graph

from graphoire.component import isConnected

def isConnectedAcyclic(G: Graph):
    """
    Return True if the graph is connected and acyclic
    """
    return isConnected(G) and len(G.edges) == G.order() - 1

def isTree(graph: Graph):
    """
    This method is an alias for isConnectedAcyclic()
    """
    return isConnectedAcyclic(graph)

def findLeaf(G: Graph):
    """
    Find and return a leaf vertex.

    Parameters
    ----------
    G : a Graph object.

    Returns
    -------
    A leaf vertex, as an int (index); returns -1 if no leaf is found.

    """
    for vertex in range(0, G.order()):
        if G.vertexDegree(vertex) == 1:
            return vertex
    return -1
    
def findAllLeaves(G: Graph):
    """
    Find all leaves of the graph
    

    Parameters
    ----------
    G : a Graph object

    Returns
    -------
    A list of int vertex indices with degree 1; returns an empty list
    if no leaves are found.
    
    Note
    ----
    The graph need not be a tree; this just returns all vertices
    with degree exactly equal to 1.
    """
    leaves = []
    for vertex in range(0, G.order()):
        if G.vertexDegree(vertex) == 1:
            leaves.append(vertex)
    return leaves


