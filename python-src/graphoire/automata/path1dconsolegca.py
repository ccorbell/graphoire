#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 17:33:35 2022

@author: mathaes
"""

from graphoire.automata.automaton import Client, Automaton
from graphoire.automata.pathrule import PathRule
from graphoire.graphfactory import GraphFactory
from graphoire.graph import Graph

class Path1DConsoleGCA(Client, Automaton):
    
    def __init__(self, 
                 graphOrder, 
                 ruleNumber, 
                 onVertices,
                 makeCycle=True):
        
        self.ruleNumber = ruleNumber
        
        g = None
        if makeCycle:
            g = GraphFactory.makeCycle(graphOrder)
        else:
            g = GraphFactory.makePath(graphOrder)
            
        for vtx in range(0, graphOrder):
            g.setVertexWeight(vtx, 0)
            
        self.graph = g
        pattern = PathRule.make1DPattern(ruleNumber)
        self.rule = PathRule(pattern)
        #Automaton.__init__(self, g, pattern)
        
        self.setInitialState(onVertices)
        
        
    def setRule(self, ruleNumber):
        pattern = PathRule.make1DPattern(ruleNumber)
        self.rule = PathRule(pattern)
        
    def setInitialState(self, onVertices):
        
        for vtx in range(0, self.graph.order()):
            self.graph.setVertexWeight(vtx, 0)
            
        for vtx in onVertices:
            self.graph.setVertexWeight(vtx, 1)
            
    def run(self, maxSteps=25):
        self.printGraphLine(self.graph)
        Automaton.run(self, maxSteps, False, self)
        
    def printGraphLine(self, graph):
        outStr = ""
        for i in range(0, graph.order()):
            weight = graph.getVertexWeight(i)
            if weight == 0:
                outStr += " "
            else:
                outStr += "*"
        print(outStr)
        
    def stepComplete(self, graph):
        self.printGraphLine(graph)
    
    def runComplete(self, graph):
        print(f"\ndone - rule {self.ruleNumber}\n")
        
            