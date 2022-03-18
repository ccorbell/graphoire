#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 15:10:11 2022

@author: mathaes
"""

from graphoire.graph import Graph

from graphoire.automata.rule import Rule

class PathRule(Rule):
    
    def __init__(self, patterns):
        self.patterns = patterns
        super().__init__()
        
    def determineVertexChange(self, graph: Graph, vertex: int):
        neighbors = graph.getNeighbors(vertex)
        vtxWeight = graph.getVertexWeight(vertex)
        
        if len(neighbors) < 2:
            # we don't change endpoints
            self.vertexChages[vertex] = vtxWeight
        else:
            leadingWeight = graph.getVertexWeight(neighbors[0])
            trailingWeight = graph.getVertexWeight(neighbors[1])
            key = (leadingWeight, vtxWeight, trailingWeight)
            
            if key in self.patterns:
                newValue = self.patterns[key]
                self.vertexChanges[vertex] = newValue
            else:
                # throw exception?
                print(f"ERROR: no pattern key for {key}")
        
    def make1DPattern(value: int):
        """
        Make a 1D cellular automata pattern from
        integer value, suitable for use by this class. Input value will 
        be constrainted to 8-bit and pattern constructed by familiar Wolfram 
        number approach.

        Parameters
        ----------
        value : int
            An 8-bit integer (0-255).

        Returns
        -------
        pattern : a dictionary of tuples to values
            The keys are tuples of zeroes and ones covering
            the eight binary triples: (1,1,1), (1,1,0), etc.
            
            The values are 0 or 1.

        """
        value = value % 256
        bstr = "{0:08b}".format(value)
        pattern = {}
        n = 7
        while n >= 0:
            nstr = "{0:03b}".format(n)
            key = (int(nstr[0]), int(nstr[1]), int(nstr[2]))
            value = int(bstr[7-n])
            pattern[key] = value
            n -= 1
        print(f"DEBUG - returning pattern {pattern}")
        return pattern
    
    