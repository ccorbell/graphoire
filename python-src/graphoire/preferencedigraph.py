#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 08:03:49 2021

@author: Christopher Corbell
"""

from graphoire.digraph import Digraph
from graphoire.labels import makeIncrementingLabelsWithPrefix


class PreferenceDigraph(Digraph):
    """
    A PreferenceDigraph is a K_r,r complete bipartite digraph,
    where vertices in each partition have weighted directed edges to
    every vertex in the other partition. The size of each partition is
    the 'suborder', which is a constructor parameter and is stored
    as an object attribute. 
    
    Vertices are labeled. If auto-labeling is used, one partition is
    labeled L0, L1, L2, ..., Ln, the other as R0, R1, R2... Rn.
    
    The edges from a vertex to all potential matches are weighted.
    The default scheme used is to weight each edge uniquely with an
    integer from 0 to suborder-1, so first preference has weight 0 and
    preferences simply represent a unique ordering.
    
    It would be possible to use different weighting schemes but the
    automatic labeling, setPreferences and getSortedPreferences methods
    assume this incrementing-integer-weight approach.
    """
    def __init__(self,
                 suborder:int,
                 autolabel:bool=True,
                 left_labels=[],
                 right_labels=[]):
        
        Digraph.__init__(self, suborder+suborder)
        
        # although we could calcuate from N or by checking size,
        # we store suborder for quick constraint validation later on
        self.suborder = suborder
        
        self.left_labels = None
        self.right_labels = None
        if True == autolabel:
            self.left_labels = makeIncrementingLabelsWithPrefix('L', suborder)
            self.right_labels = makeIncrementingLabelsWithPrefix('R', suborder)
        else:
            self.left_labels = left_labels
            self.right_labels = right_labels
            
        # assign labels
        for offset in range(0, suborder):
            left_vtx = offset
            right_vtx = offset + suborder
            self.setVertexLabel(left_vtx, left_labels[offset])
            self.setVertexLabel(right_vtx, right_labels[offset])
            
        # set bipartite directed edges
        for v1 in range(0, suborder):
            for v2 in range(suborder, suborder + suborder):
                self.addEdge(v1, v2)
                self.addEdge(v2, v1)
                
        self.sortEdges()
        
    def setPreferences(self, selector_label, preference_labels):
        """
        Set preferences by label. The preferences of the selector
        are expected to be ordered from most-preferred to least in
        preference_labels. These are recorded as edge-weights, where
        a weight of 0 is most-preferred.

        Parameters
        ----------
        selector_label : string
            The label of the selector (preference subject).
        preference_labels : list
            The preference-ordered labels of the selector's choices.

        Raises
        ------
        Exception
            Invalid parameter if preference_labels is the wrong size, labels not found, or sim.

        """
        if len(preference_labels) != self.suborder:
            raise Exception(f"Invalid parameter: preference_labels must have size {self.suborder}")
            
        left_vtx = self.getVertexByLabel(selector_label)
        if None == left_vtx:
            raise Exception(f"Invalid parameter - no selector vertex with label {selector_label}")
        
        vtxbag = set()
        for n in range(0, len(preference_labels)):
            right_vtx = self.getVertexByLabel(preference_labels[n])
            if None == right_vtx:
                raise Exception(f"Invalid parameter - no target vertex with label {preference_labels[n]}")
            if right_vtx in vtxbag:
                raise Exception(f"Invalid parameter - vertex label {preference_labels[n]} used more than once in list.")
            vtxbag.add(right_vtx)
            
            self.setEdgeWeight(left_vtx, right_vtx, n)
        
        
    def getSortedPreferences(self, selector_label):
        """
        Get preference relations by label, ordered by assigned weight.

        Parameters
        ----------
        selector_label : TYPE
            DESCRIPTION.

        Returns
        -------
        The labels ov the vertices that are out-neighbors of selector, sorted by edge weight.

        """
        selector_vtx = self.getVertexByLabel(selector_label)
        if None == selector_vtx:
            raise Exception(f"Invalid parameter - no selector vertex with label {selector_label}")
        neighbors = self.getOutNeighbors(selector_vtx)
        if len(neighbors) != self.suborder:
            raise Exception(f"Invalid state - object has suborder {self.suborder} but vertex {selector_label} only has {len(neighbors)} out-neighbors.")
        neighborWeights = []
        for neighbor in neighbors:
            weight = self.getEdgeWeight(selector_vtx, neighbor)
            if None == weight:
                raise Exception(f"Invalid state - neighbor of {selector_label} has no edge weight assigned - edge [{selector_vtx}, {neighbor}]")
            neighborWeights.append(weight)
        sortedNeighbors = [vtx for _,vtx in sorted(zip(neighborWeights, neighbors))]
        sortedLabels = []
        for vtx in sortedNeighbors:
            label = self.getVertexLabel(vtx)
            if None == label:
                raise Exception(f"Invalid state - neighbor vertex {vtx} has no label.")
            sortedLabels.append(label)
        return sortedLabels
        
        
    
    
    
    
    