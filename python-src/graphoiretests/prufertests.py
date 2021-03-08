#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 12:22:21 2021

@author: mathaes
"""

import unittest

from graphoire.graphfactory import GraphFactory
from graphoire.prufer import createPruferCode

def RunAllPruferTests():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCreatePruferCode))

    runner = unittest.TextTestRunner()
    runner.run(suite)
    
def prufertests_main():
    unittest.main()
    
class TestCreatePruferCode(unittest.TestCase):
    
    def testBasicSuccess(self):
        tree = GraphFactory.makePath(9)
        tree.deleteEdge([3, 4])
        tree.deleteEdge([7, 8])
        tree.addEdge(2, 5)
        tree.addEdge(6, 8)
        
        pcode = createPruferCode(tree)
        #print (pcode)
        
        self.assertEqual(['2', '3', '4', '6', '7', '7', '9'], pcode)
        # check that original tree is not changed
        self.assertEqual(9, tree.order())
        
        
if __name__ == "__main__":
    prufertests_main()