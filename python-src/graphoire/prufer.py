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
    # Make a copy of the graph that we can label and destroy
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
            labelInt = int(leafLabel) # we need to sort on label as an integer
            labelLeafTuples.append((labelInt, leafIndex))
            
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

