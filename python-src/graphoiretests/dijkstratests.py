#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 10:10:59 2021

@author: mathaes
"""

import unittest

from graphoire.algorithm.dijkstra import *
from graphoire.graphfactory import GraphFactory


def RunAllDijkstraTests():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestDijkstra))

    runner = unittest.TextTestRunner()
    runner.run(suite)
    
def Run1DijkstraTest(name):
    suite = unittest.TestSuite()
    suite.addTest(TestDijkstra(name))

    runner = unittest.TextTestRunner()
    runner.run(suite)
    
def dijkstratests_main():
    unittest.main()

class TestDijkstra(unittest.TestCase):
    
    def testFindAllPaths_emptyGraph(self):
        g = GraphFactory.makeEmpty(5)
        djk = Dijkstra(g)
        results = djk.findAllLeastCostPaths(0)
        
        self.assertEqual(0, results[0])
        for n in range(1, 5):
            self.assertEqual(math.inf, results[n])
            
    
    def testTrivial(self):
        pass
    
    def testBasicGraph(self):
        pass
    
    def testUniformGraph(self):
        pass
    
    def testBasicDigraph(self):
        pass
    
    
if __name__ == "__main__":
    dijkstratests_main()
