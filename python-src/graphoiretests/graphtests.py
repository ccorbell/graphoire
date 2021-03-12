#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 16:18:44 2021

@author: mathaes
"""

import unittest

from graphoire.graph import Graph
from graphoire.graphfactory import GraphFactory

def RunAllGraphTests():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestGraphBasics))
    suite.addTest(unittest.makeSuite(TestGraphConstructions))
    suite.addTest(unittest.makeSuite(TestGraphMatrices))

    runner = unittest.TextTestRunner()
    runner.run(suite)
    
def Run1GraphBasicsTest(name):
    suite = unittest.TestSuite()
    suite.addTest(TestGraphBasics(name))

    runner = unittest.TextTestRunner()
    runner.run(suite)
    
def graphtests_main():
    unittest.main()
    
class TestGraphBasics(unittest.TestCase):
    
    def testInitEmpty(self):
        G0 = Graph(0)
        self.assertEqual(0, G0.n)
        self.assertEqual(0, G0.order())
        self.assertEqual(0, len(G0.edges))
        
        G123 = Graph(123)
        self.assertEqual(123, G123.n)
        self.assertEqual(123, G123.order())
        self.assertEqual(0, len(G123.edges))
        
    def testVertexDegree(self):
        G = Graph(5)
        
        self.assertEqual(0, G.vertexDegree(1))
        self.assertEqual(0, G.vertexDegree(4))
        
        G.addEdge(0, 1)
        G.addEdge(0, 2)
        G.addEdge(0, 3)
        G.addEdge(3, 4)
        
        self.assertEqual(3, G.vertexDegree(0))
        self.assertEqual(1, G.vertexDegree(1))
        self.assertEqual(1, G.vertexDegree(2))
        self.assertEqual(2, G.vertexDegree(3))
        self.assertEqual(1, G.vertexDegree(4))
        
    def testDegreeMin(self):
        G = Graph(5)
        self.assertEqual(0, G.degreeMin())
        
        G.addEdge(0, 1)
        G.addEdge(0, 2)
        G.addEdge(0, 3)
        self.assertEqual(0, G.degreeMin())
        
        G.addEdge(1, 3)
        G.addEdge(2, 3)
        G.addEdge(3, 4)
        self.assertEqual(1, G.degreeMin())
        
        C8 = GraphFactory.makeCycle(8)
        self.assertEqual(2, C8.degreeMin())
        
        K7 = GraphFactory.makeComplete(7)
        self.assertEqual(6, K7.degreeMin())

    
    def testDegreeMax(self):
        G = Graph(5)
        self.assertEqual(0, G.degreeMax())
        
        G.addEdge(0, 1)
        G.addEdge(0, 2)
        G.addEdge(0, 3)
        self.assertEqual(3, G.degreeMax())
        
        G.addEdge(1, 3)
        G.addEdge(2, 3)
        G.addEdge(3, 4)
        self.assertEqual(4, G.degreeMax())
        
        C8 = GraphFactory.makeCycle(8)
        self.assertEqual(2, C8.degreeMax())
        
        K7 = GraphFactory.makeComplete(7)
        self.assertEqual(6, K7.degreeMax())
        
        
    def testDegreeSum(self):
        G = Graph(5)
        self.assertEqual(0, G.degreeSum())
        
        G.addEdge(0, 1)
        G.addEdge(0, 2)
        G.addEdge(0, 3)
        G.addEdge(1, 4)
        G.addEdge(3, 4)
        self.assertEqual(10, G.degreeSum())
        
        C8 = GraphFactory.makeCycle(8)
        self.assertEqual(8 * 2, C8.degreeSum())
        
        K7 = GraphFactory.makeComplete(7)
        self.assertEqual(7 * 6, K7.degreeSum())

    
    def testDegreeAvg(self):
        G = Graph(5)
        self.assertEqual(0.0, G.degreeAvg())
        
        expected = [0, 0, 0, 0, 0]
        self.assertEqual(expected, G.degreeSequence())
        
        G.addEdge(0, 1)
        G.addEdge(0, 2)
        G.addEdge(0, 3)
        G.addEdge(1, 4)
        G.addEdge(3, 4)
        
        expected = [3, 2, 2, 2, 1]
        self.assertEqual(expected, G.degreeSequence())
        
        P4 = GraphFactory.makePath(4)
        expected = [2, 2, 1, 1]
        self.assertEqual(expected, P4.degreeSequence())
        
        Pet = GraphFactory.makePetersen()
        expected = [3] * 10
        self.assertEqual(expected, Pet.degreeSequence())
        
    
    def testDegreeSequence(self):
        
        pass
    
    def testHasEdge(self):
        pass
    
    def testAddEdge(self):
        pass
    
    def testSortEdges(self):
        pass
    
    def testDeleteVertex(self):
        pass
    
    def testDeleteEdge(self):
        pass
    
    def testGetEdgesForVertex(self):
        pass
    
    def testGetNeighbors(self):
        pass
    
    def testIsEven(self):
        pass
    
    def testIsComplete(self):
        pass
    
class TestGraphConstructions(unittest.TestCase):
    
    def testComplement(self):
        pass
    
    def testInducedSubgraph(self):
        pass
    
class TestGraphMatrices(unittest.TestCase):
    
    def testAdjacencyMatrix(self):
        pass
    
    def testEdgeVertexMatrix(self):
        pass
    
    def testIncidenceMatrix(self):
        pass
        

if __name__ == "__main__":
    graphtests_main()