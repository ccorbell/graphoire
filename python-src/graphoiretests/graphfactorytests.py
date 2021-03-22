#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 12:02:01 2021

@author: mathaes
"""

import unittest

from graphoire.graph import Graph
from graphoire.graphfactory import GraphFactory
from graphoire.component import isConnected
from graphoire.tree import isTree

def RunAllGraphFactoryTests():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestGraphFactory))

    runner = unittest.TextTestRunner()
    runner.run(suite)
    
def Run1GraphBasicsTest(name):
    suite = unittest.TestSuite()
    suite.addTest(TestGraphFactory(name))

    runner = unittest.TextTestRunner()
    runner.run(suite)
    
def graphfactorytests_main():
    unittest.main()
    
class TestGraphFactory(unittest.TestCase):
    
    def testMakeRandomTree(self):
        
        T2 = GraphFactory.makeRandomTree(2)
        self.assertEqual(2, T2.order())
        self.assertEqual(1, T2.edgeCount())
        self.assertEqual([0, 1], T2.edges[0])
        self.assertTrue(isTree(T2))
        
        T10a = GraphFactory.makeRandomTree(10)
        self.assertEqual(10, T10a.order())
        self.assertEqual(9, T10a.edgeCount())
        self.assertTrue(isTree(T10a))
        
        T10b = GraphFactory.makeRandomTree(10)
        self.assertEqual(10, T10b.order())
        self.assertEqual(9, T10b.edgeCount())
        self.assertTrue(isTree(T10b))
        self.assertNotEqual(T10a.edges, T10b.edges)
        
        T25_max4 = GraphFactory.makeRandomTree(25, 4)
        self.assertEqual(25, T25_max4.order())
        self.assertEqual(24, T25_max4.edgeCount())
        for vertex in range(0, T25_max4.order()):
            deg = T25_max4.vertexDegree(vertex)
            self.assertTrue(deg > 0)
            self.assertTrue(deg <= 4)
        
if __name__ == "__main__":
    graphfactorytests_main()