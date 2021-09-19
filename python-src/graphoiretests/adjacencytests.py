#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 28 18:18:27 2021

@author: mathaes
"""

import unittest
from graphoire.linalg.adjacency import *
from graphoire.graphfactory import GraphFactory

def adjacencytests_main():
    unittest.main()
    
class TestAdjacency(unittest.TestCase):
    
    def testFromGraph(self):
        K5 = GraphFactory.makeComplete(5)
        K5Adj = Adjacency.fromGraph(K5)
        self.assertFalse(None == K5Adj)
        self.assertFalse(None == K5Adj.A)
        #print(C5Adj.A)
        npA = K5Adj.A.todense()
        print(npA)
        #@print(C5Adj.A.todense())
        
    def testPower(self):
        C5 = GraphFactory.makeCycle(5)
        C5Adj = Adjacency.fromGraph(C5)
        self.assertFalse(None == C5Adj)
        self.assertFalse(None == C5Adj.A)
        
        C5CubedAdj = C5Adj.power(3)
        print(C5CubedAdj.A)
        #npC53d = C5CubedAdj.A.todense()
        #print(npnpC53d)
        
    def testEigenvalues(self):
        pass
    
    
        

if __name__ == "__main__":
    adjacencytests_main()
    