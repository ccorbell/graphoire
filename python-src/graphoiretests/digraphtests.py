#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 09:57:34 2021

@author: Christopher Corbell
"""

import unittest

from graphoire.digraph import Digraph

def RunAllDiraphTests():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestDigraphs))
    runner = unittest.TextTestRunner()
    runner.run(suite)
    
def Run1DigraphTest(name):
    suite = unittest.TestSuite()
    suite.addTest(TestDigraphs(name))

    runner = unittest.TextTestRunner()
    runner.run(suite)
    
def digraphtests_main():
    unittest.main()
    
class TestDigraphs(unittest.TestCase):
    
    def testDigraphBasics(self):
        dig = Digraph(10)
        self.assertTrue(dig.directed)
        self.assertEqual(10, dig.order())
        
        # show we can set edges in both direction between to vertices
        dig.addEdge(2, 1)
        dig.addEdge(1, 2)
        dig.sortEdges()
        
        self.assertEqual(2, dig.edgeCount())
        self.assertTrue(dig.hasEdge(2, 1))
        self.assertTrue(dig.hasEdge(1, 2))
        
        dig.deleteEdge([1, 2])
        
        self.assertEqual(1, dig.edgeCount())
        self.assertTrue(dig.hasEdge(2, 1))
        self.assertFalse(dig.hasEdge(1, 2))
        
    def testVertexInAndOutDegrees(self):
        dig = Digraph(5)
        dig.addEdge(0, 1)
        dig.addEdge(0, 2)
        dig.addEdge(0, 3)
        dig.addEdge(4, 3)
        dig.addEdge(1, 2)
        
        dig.sortEdges()
        
        #print (dig)
        
        self.assertEqual(0, dig.vertexInDegree(0))
        self.assertEqual(3, dig.vertexOutDegree(0))
        
        self.assertEqual(1, dig.vertexInDegree(1))
        self.assertEqual(1, dig.vertexOutDegree(1))
        
        self.assertEqual(2, dig.vertexInDegree(2))
        self.assertEqual(0, dig.vertexOutDegree(2))
        
        self.assertEqual(2, dig.vertexInDegree(3))
        self.assertEqual(0, dig.vertexOutDegree(3))
        
        self.assertEqual(0, dig.vertexInDegree(4))
        self.assertEqual(1, dig.vertexOutDegree(4))
        
    def testGetUnderlyingGraph(self):
        dig = Digraph(4)
        dig.addEdge(0, 1)
        dig.addEdge(1, 2)
        dig.addEdge(2, 3)
        dig.addEdge(3, 0)
        dig.addEdge(0, 2)
        dig.addEdge(3, 1)
        dig.addEdge(1, 3)
        dig.sortEdges()
        
        self.assertTrue(dig.directed)
        self.assertEqual(7, dig.edgeCount())
        self.assertEqual(4, dig.order())
        self.assertTrue(dig.hasEdge(1, 3))
        self.assertTrue(dig.hasEdge(3, 1))
        self.assertTrue(dig.hasEdge(3, 0))
        self.assertFalse(dig.hasEdge(0, 3))
        
        underG = dig.getUnderlyingGraph()
        self.assertFalse(underG.directed)
        self.assertEqual(6, underG.edgeCount())
        self.assertEqual(4, underG.order())
        self.assertTrue(underG.isComplete())
        
        self.assertTrue(underG.hasEdge(1, 3))
        self.assertTrue(underG.hasEdge(3, 1))
        self.assertTrue(underG.hasEdge(3, 0))
        self.assertTrue(underG.hasEdge(0, 3))
        

if __name__ == "__main__":
    digraphtests_main()