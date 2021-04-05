#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 15:05:38 2021

@author: mathaes
"""

import unittest

from graphoire.algorithm.fordfulkerson import FordFulkerson
from graphoire.network import Network

def RunAllFordFulkersonTests():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestFordFulkerson))

    runner = unittest.TextTestRunner()
    runner.run(suite)
    
def Run1FordFulkersonTest(name):
    suite = unittest.TestSuite()
    suite.addTest(TestFordFulkerson(name))

    runner = unittest.TextTestRunner()
    runner.run(suite)
    
def fordfulkersontests_main():
    unittest.main()
    
    
class TestFordFulkerson(unittest.TestCase):
    
    
    def testWith432(self):
        # make network with 9 vertices, s=0, t=8
        network = Network(9, 0, 8)
    
        # add edges with capacities
        network.addNetworkEdge(0, 1, 5)
        network.addNetworkEdge(0, 3, 14)
        network.addNetworkEdge(1, 2, 4)
        network.addNetworkEdge(1, 4, 5)
        network.addNetworkEdge(1, 5, 4)
        network.addNetworkEdge(2, 5, 3)
        network.addNetworkEdge(3, 1, 13)
        network.addNetworkEdge(3, 6, 5)
        network.addNetworkEdge(3, 7, 2)
        network.addNetworkEdge(4, 3, 6)
        network.addNetworkEdge(4, 7, 6)
        network.addNetworkEdge(5, 4, 4)
        network.addNetworkEdge(5, 7, 3)
        network.addNetworkEdge(5, 8, 6)
        network.addNetworkEdge(6, 7, 3)
        network.addNetworkEdge(7, 8, 12)
        
        ff = FordFulkerson(network)
        #print(ff)
        
        foundFlow = ff.run()
        #print(ff)
        
        self.assertTrue(foundFlow)
        totalFlow = ff.getTotalFlow()
        
        cutFlow = ff.getMinimumCutFlow()
        
        self.assertEqual(17, totalFlow)
        self.assertEqual(17, cutFlow)        
            
    def testTrivial1_singlePath(self):
        network = Network(4, 0, 3)
        network.addNetworkEdge(0, 1, 3)
        network.addNetworkEdge(1, 2, 2)
        network.addNetworkEdge(2, 3, 4)
        
        ff = FordFulkerson(network)
        #print(ff)
        
        foundFlow = ff.run()
        #print(ff)
        
        self.assertTrue(foundFlow)
        self.assertEqual(2, ff.getTotalFlow())
        self.assertEqual(2, ff.getMinimumCutFlow())        
    
    def testTrivial2_simpleCycle(self):
        network = Network(5, 0, 4)
        network.addNetworkEdge(0, 1, 3)
        network.addNetworkEdge(1, 4, 1)
        network.addNetworkEdge(0, 2, 2)
        network.addNetworkEdge(2, 3, 1)
        network.addNetworkEdge(3, 4, 3)
        
        ff = FordFulkerson(network)
        #print(ff)
        
        foundFlow = ff.run()
        #print(ff)
        
        self.assertTrue(foundFlow)
        self.assertEqual(2, ff.getTotalFlow())
        self.assertEqual(2, ff.getMinimumCutFlow())  
    
    def testTrivial3_K4_var1(self):
        network = Network(4, 0, 2)
        network.addNetworkEdge(0, 1, 3)
        network.addNetworkEdge(0, 2, 1)
        network.addNetworkEdge(0, 3, 1)
        network.addNetworkEdge(1, 2, 1)
        network.addNetworkEdge(1, 3, 2)
        network.addNetworkEdge(3, 2, 3)
        
        ff = FordFulkerson(network)
        #print(ff)
        foundFlow = ff.run()
        #print(ff)
        self.assertTrue(foundFlow)
        totalFlow = ff.getTotalFlow()
        self.assertEqual(5, totalFlow)
        cutFlow = ff.getMinimumCutFlow()
        self.assertEqual(5, cutFlow)  

    def testTrivial3_K4_var2(self):
        network = Network(4, 0, 2)
        network.addNetworkEdge(0, 1, 4)
        network.addNetworkEdge(0, 2, 1)
        network.addNetworkEdge(0, 3, 1)
        network.addNetworkEdge(1, 2, 1)
        network.addNetworkEdge(1, 3, 2)
        network.addNetworkEdge(3, 2, 3)
        
        ff = FordFulkerson(network)
        #print(ff)
        foundFlow = ff.run()
        #print(ff)
        self.assertTrue(foundFlow)
        totalFlow = ff.getTotalFlow()
        self.assertEqual(5, totalFlow)
        cutFlow = ff.getMinimumCutFlow()
        self.assertEqual(5, cutFlow)  
    
    def testSetEdgeFlow(self):
        network = Network(4, 0, 3)
        network.addNetworkEdge(0, 1, 3)
        network.addNetworkEdge(0, 2, 3)
        network.addNetworkEdge(1, 2, 3)
        network.addNetworkEdge(1, 3, 1)
        network.addNetworkEdge(2, 3, 3)
        
        ff = FordFulkerson(network)
        self.assertEqual(5, len(ff.edgeFlows))
        
        self.assertEqual(0, ff.getEdgeFlow(0, 1))
        self.assertEqual(0, ff.getEdgeFlow(1, 3))
        ff.setEdgeFlow(0, 1, 1)
        ff.setEdgeFlow(1, 3, 1)
        self.assertEqual(1, ff.getEdgeFlow(0, 1))
        self.assertEqual(1, ff.getEdgeFlow(1, 3))
        
            
    def testZeroEdgeFlows(self):
        network = Network(5, 0, 4)
        
        network.addNetworkEdge(0, 1, 3)
        network.addNetworkEdge(0, 2, 4)
        network.addNetworkEdge(1, 2, 1)
        network.addNetworkEdge(2, 3, 4)
        network.addNetworkEdge(3, 1, 1)
        network.addNetworkEdge(3, 4, 3)
        network.addNetworkEdge(1, 4, 1)
        
        ff = FordFulkerson(network)
        self.assertEqual(7, len(ff.edgeFlows))
        
        ff.edgeFlows[str([0, 1])] = 1
        ff.edgeFlows[str([1, 2])] = 1
        ff.edgeFlows[str([2, 3])] = 1
        ff.edgeFlows[str([3, 4])] = 1
        
        self.assertEqual(7, len(ff.edgeFlows))
        
        
        ff.zeroEdgeFlows()
        self.assertEqual(7, len(ff.edgeFlows))
        
if __name__ == "__main__":
    fordfulkersontests_main()
    