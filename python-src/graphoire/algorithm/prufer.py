#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 11:17:26 2021

@author: Christopher Corbell
"""
from graphoire.graph import Graph
from graphoire.tree import findAllLeaves
from graphoire.labels import labelGraphVerticesWithIntegers

import copy

def createPruferCode(G:Graph):
    """
    Create a Prüfer code for a given Graph object.

    Parameters
    ----------
    G : a Graph object.

    Raises
    ------
    Exception
        Raises if the algorithm cannot find leaves, which may happen if the 
        graph is not a tree.

    Returns
    -------
    code : array of integer vertex label values

    Behavior
    --------
    The algorithm creates a copy of the input graph on which it operates.
    It first labels the graph using 1-based integer-value labels. Then
    it applies the Prufer-code algorithm, finding lowest-label-valued leaf
    and recording its neighbor's label, then deleting the leaf, etc.,
    until only two vertices remain.
    
    So the return value is an integer sequence (returned as a python list)
    built from one-based vertex labels.
    """
    # Make a copy of the graph that we can label and delete vertices
    Gcopy = copy.copy(G)
    
    # we need one-based integer-incrementing labels on all the vertices
    labelGraphVerticesWithIntegers(Gcopy, addValue=1)
    
    code = []
    
    while Gcopy.order() > 2:

        # find the lowest-labeled leaf
        leafIndices = findAllLeaves(Gcopy)
        labelLeafTuples = []
        for leafIndex in leafIndices:
            leafLabel = Gcopy.getVertexLabel(leafIndex)
            if None == leafLabel:
                raise Exception(f"Error, no leaf label found for leaf index {leafIndex}")
            labelLeafTuples.append((leafLabel, leafIndex))
            
        if len(labelLeafTuples) == 0:
            # Error - maybe the graph was not a tree?
            # No leaves found
            raise Exception(f"Error, no leaves found in graph at size {Gcopy.order()}; it may not be a tree.")
            
        labelLeafTuples.sort()
        # the first item is now the lowest-labeled leaf vertex
        lowestLeafVertex = labelLeafTuples[0][1]
        leafNeighbors = Gcopy.getNeighbors(lowestLeafVertex)
        if len(leafNeighbors) != 1:
            raise Exception(f"Unexpected error, {len(leafNeighbors)} neighbors found for leaf-vertex.")
            
        neighborLabel = Gcopy.getVertexLabel(leafNeighbors[0])
        code.append(neighborLabel)
        
        # Now remove this leaf and continue
        Gcopy.deleteVertex(lowestLeafVertex)
        
    return code
    
def graphFromPruferCode(code):
    pass

