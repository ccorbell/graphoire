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
import math

def RunAllGraphFactoryTests():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestGraphFactory))

    runner = unittest.TextTestRunner()
    runner.run(suite)
    
def Run1GraphFactoryTest(name):
    suite = unittest.TestSuite()
    suite.addTest(TestGraphFactory(name))

    runner = unittest.TextTestRunner()
    runner.run(suite)
    
def graphfactorytests_main():
    unittest.main()
    
class TestGraphFactory(unittest.TestCase):
    
    def testMakePath(self):
        P37 = GraphFactory.makePath(37)
        self.assertEqual(37, P37.order())
        self.assertEqual(36, P37.edgeCount())
        self.assertTrue(isConnected(P37))
        
        leafCount = 0
        for vertex in range(0, P37.order()):
            deg = P37.vertexDegree(vertex)
            if deg == 1:
                leafCount += 1
            elif deg != 2:
                self.fail(f"vertex {vertex} has degree {deg}, graph should be a path")
        self.assertEqual(2, leafCount)
        
    def testMakeCycle(self):
        C11 = GraphFactory.makeCycle(11)
        self.assertEqual(11, C11.order())
        self.assertEqual(11, C11.edgeCount())
        self.assertTrue(isConnected(C11))
        self.assertFalse(isTree(C11))
        for vertex in range(0, C11.order()):
            self.assertEqual(2, C11.vertexDegree(vertex))
            
    def testMakeComplete(self):
        K5 = GraphFactory.makeComplete(5)
        self.assertEqual(5, K5.order())
        self.assertEqual(10, K5.edgeCount())
        self.assertTrue(isConnected(K5))
        self.assertFalse(isTree(K5))
        for vertex in range(0, K5.order()):
            self.assertEqual(4, K5.vertexDegree(vertex))
            
        K17 = GraphFactory.makeComplete(17)
        self.assertEqual(17, K17.order())
        self.assertEqual(136, K17.edgeCount())
        self.assertTrue(isConnected(K17))
        self.assertFalse(isTree(K17))
        for vertex in range(0, K17.order()):
            self.assertEqual(16, K17.vertexDegree(vertex))    
    
    def testMakeBipartiteComplete(self):
        K_4_3 = GraphFactory.makeBipartiteComplete(4, 3)
        self.assertEqual(7, K_4_3.order())
        self.assertEqual(4 * 3, K_4_3.edgeCount())
        self.assertEqual(3, K_4_3.degreeMin())
        self.assertEqual(4, K_4_3.degreeMax())
        
        degree_3_count = 0
        degree_4_count = 0
        for vertex in range(0, K_4_3.order()):
            deg = K_4_3.vertexDegree(vertex)
            if deg == 3:
                degree_3_count += 1
            elif deg == 4:
                degree_4_count += 1
            else:
                self.fail(f"Found degree {deg} in bipartite graph, should only have 3 or 4")
        self.assertEqual(4, degree_3_count)
        self.assertEqual(3, degree_4_count)
        
    def testMakeKPartiteComplete(self):
        K_5_3_2 = GraphFactory.makeKPartiteComplete([5, 3, 2])
        self.assertEqual(5 + 3 + 2, K_5_3_2.order())
        self.assertEqual(5*3 + 5*2 + 3*2, K_5_3_2.edgeCount())
        self.assertEqual(5+3, K_5_3_2.degreeMax())
        self.assertEqual(2+3, K_5_3_2.degreeMin())
        self.assertEqual(5*(3+2) + 3*(5+2) + 2*(5+3), K_5_3_2.degreeSum())
        deg_5_count = 0
        deg_7_count = 0
        deg_8_count = 0
        for vertex in range(0, K_5_3_2.order()):
            deg = K_5_3_2.vertexDegree(vertex)
            if deg == 5:
                deg_5_count += 1
            elif deg == 7:
                deg_7_count += 1
            elif deg == 8:
                deg_8_count += 1
            else:
                self.fail(f"Found degree {deg} in k-partite graph, expected 5, 7, or 8")
        self.assertEqual(5, deg_5_count)
        self.assertEqual(3, deg_7_count)
        self.assertEqual(2, deg_8_count)
        
    def testMakeTuranGraph(self):
        T_12_3 = GraphFactory.makeTuranGraph(12, 3)
        self.assertEqual(12, T_12_3.order())
        self.assertEqual(8, T_12_3.degreeMax())
        self.assertEqual(8, T_12_3.degreeMin())
        self.assertEqual((8 * 12) / 2, T_12_3.edgeCount())
        
        T_11_3 = GraphFactory.makeTuranGraph(11, 3)
        self.assertEqual(11, T_11_3.order())
        self.assertEqual(8, T_11_3.degreeMax())
        self.assertEqual(7, T_11_3.degreeMin())
        self.assertEqual((8*3 + 7*8) / 2, T_11_3.edgeCount())
        
        T_174_19 = GraphFactory.makeTuranGraph(174, 19)
        self.assertEqual(174, T_174_19.order())
        degreeCounts = {}
        for vertex in range(0, T_174_19.order()):
            deg = T_174_19.vertexDegree(vertex)
            if deg in degreeCounts:
                degreeCounts[deg] = degreeCounts[deg] + 1
            else:
                degreeCounts[deg] = 1
        
        self.assertEqual(2, len(degreeCounts))
        self.assertTrue(164 in degreeCounts)
        self.assertTrue(165 in degreeCounts)
        self.assertEqual(degreeCounts[164] + degreeCounts[165], T_174_19.order())
        degreeSum = 164 * degreeCounts[164] + 165 * degreeCounts[165]
        self.assertEqual(degreeSum/2, T_174_19.edgeCount())

        
    def testMakeHouse(self):
        house = GraphFactory.makeHouse()
        self.assertEqual(5, house.order())
        self.assertEqual(6, house.edgeCount())
        degree_2_count = 0
        degree_3_count = 0
        
        for vertex in range(0, house.order()):
            deg = house.vertexDegree(vertex)
            if deg == 2:
                degree_2_count += 1
            elif deg == 3:
                degree_3_count += 1
            else:
                self.fail("Found degree {deg} in house graph, should only have 2 or 3")
        self.assertEqual(3, degree_2_count)
        self.assertEqual(2, degree_3_count)
    
        
    def testMakeClaw(self):
        claw = GraphFactory.makeClaw()
        self.assertEqual(4, claw.order())
        self.assertEqual(3, claw.edgeCount())
        
        degree_1_count = 0
        degree_3_count = 0
        
        for vertex in range(0, claw.order()):
            deg = claw.vertexDegree(vertex)
            if deg == 1:
                degree_1_count += 1
            elif deg == 3:
                degree_3_count += 1
            else:
                self.fail("Found degree {deg} in claw graph, should only have 1 or 3")
        self.assertEqual(3, degree_1_count)
        self.assertEqual(1, degree_3_count)
        
    def testMakePetersen(self):
        pete = GraphFactory.makePetersen()
        self.assertEqual(10, pete.order())
        self.assertEqual(15, pete.edgeCount())
        self.assertEqual(3, pete.degreeMin())
        self.assertEqual(3, pete.degreeMax())
        self.assertTrue(isConnected(pete))
        
        # we should have disjoint 2-subset labels on all connected vertices
        for edge in pete.edges:
            v0 = edge[0]
            v1 = edge[1]
            v0label = pete.getVertexLabel(v0)
            v1label = pete.getVertexLabel(v1)
            self.assertEqual(2, len(set(v0label)))
            self.assertEqual(2, len(set(v1label)))
            self.assertEqual(0, len(set(v0label) & set(v1label)))
        #print(pete)
        
    def testMakeKSubsetExclusionGraph(self):
        subexG = GraphFactory.makeKSubsetExclusionGraph(7, 3)
        self.assertEqual(math.comb(7, 3), subexG.order())
        self.assertEqual(4, subexG.degreeMin())
        self.assertEqual(4, subexG.degreeMax())
        
        for edge in subexG.edges:
            v0 = edge[0]
            v1 = edge[1]
            v0label = subexG.getVertexLabel(v0)
            v1label = subexG.getVertexLabel(v1)
            self.assertEqual(3, len(set(v0label)))
            self.assertEqual(3, len(set(v1label)))
            self.assertEqual(0, len(set(v0label) & set(v1label)))
        #print(subexG)
        
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