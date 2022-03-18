#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 16:42:25 2022

@author: mathaes
"""

from graphoire.graph import Graph
from graphoire.automata.rule import Rule
import copy

class Client:
    def __init__(self):
        pass
    
    def stepComplete(self, graph):
        pass
    
    def runComplete(self, graph):
        pass

class Automaton:

    def __init__(self, graph: Graph, rule: Rule):
        self.graph = graph
        self.rule = rule
        self.cachedResults = []
        
        
    def step(self, cacheResults=False, client=None):
        self.rule.applyToGraph(self.graph)
        
        if True == cacheResults:
            self.cachedResults.append(copy.deepcopy(self.graph))
            
        if None != client:
            client.stepComplete(self.graph)
            
    def run(self, maxSteps=100, cacheResults=False, client=None):
        
        for i in range(0, maxSteps):
            self.step(cacheResults, client)
            
        if None != client:
            client.runComplete(self.graph)
            
            
    
        
    

        
        