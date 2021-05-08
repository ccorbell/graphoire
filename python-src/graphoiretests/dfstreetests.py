#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  7 17:38:01 2021

@author: mathaes
"""


import unittest

import copy

from graphoire.graph import Graph
from graphoire.graphfactory import GraphFactory
from graphoire.algorithm.dfstree import dfstree, DFSTreeVisitor

def dfstreetests_main():
    unittest.main()
    
class TestDFSTree(unittest.TestCase):
    
    def XtestSimplePathSearch(self):
        expectedEdges = [[0,1], [1,2], [2,3], [3,4]]
        
        P5 = GraphFactory.makePath(5)
        edges1 = dfstree(P5, start=0)
        self.assertEqual(len(expectedEdges), len(edges1))
        for edge in expectedEdges:
            self.assertTrue(edge in edges1)
        #print (edges1)
        
        edges2 = dfstree(P5, start=2)
        self.assertEqual(len(expectedEdges), len(edges2))
        for edge in expectedEdges:
            self.assertTrue(edge in edges2)
        #print (edges2)
        
        edges3 = dfstree(P5, start=4)
        self.assertEqual(len(expectedEdges), len(edges3))
        for edge in expectedEdges:
            self.assertTrue(edge in edges3)
        #print (edges3)

    def XtestTreeSearch(self):
        tree = GraphFactory.makeRandomTree(12)
        #print (tree)
        edges = dfstree(tree, start=5)
        #print (edges)
        self.assertEqual(tree.edgeCount(), len(edges))
        for edge in tree.edges:
            self.assertTrue(edge in edges)
        
    def XtestPetersenDFS(self):
        pet = GraphFactory.makePetersen()
        #print (pet)
        edges = dfstree(pet)
        #print (f"Found DFS tree with {len(edges)} edges:\n{edges}")
        
        self.assertEqual(9, len(edges))
        # make sure every vertex is in at least one edge:
        vset = set()
        for edge in edges:
            vset.add(edge[0])
            vset.add(edge[1])
            
        self.assertEqual(10, len(vset))
        for n in range(0, 10):
            self.assertTrue(n in vset)
            
    def testCompleteDFS(self):
        K23 = GraphFactory.makeComplete(23)
        print (K23)
        
        edges = dfstree(K23, start=10, verbose=True)
        print(f"K23 DFS spanning tree edges:\n{edges}")
        self.assertEqual(22, len(edges))
        # make sure every vertex is in at least one edge:
        vset = set()
        for edge in edges:
            vset.add(edge[0])
            vset.add(edge[1])
            
        self.assertEqual(23, len(vset))
        for n in range(0, 23):
            self.assertTrue(n in vset)
        

if __name__ == "__main__":
    dfstreetests_main()