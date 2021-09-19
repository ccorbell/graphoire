#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 28 09:27:11 2021

@author: mathaes
"""

import copy

#import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigsh
from scipy.sparse import identity

from graphoire.linalg.graph2matrix import graphToAdjacencyMatrix

from graphoire.graph import Graph

class Adjacency:
    
    def fromGraph(G: Graph):
        A = graphToAdjacencyMatrix(G)
        adj = Adjacency(A)
        return adj
        
    def __init__(self, A: coo_matrix):
        self.A = A
        self.eigenvalues = None
        self.eigenvectors = None
        
    def makeEigenvalues(self):
        self.eigenvalues, self.eigenvectors = eigsh(self.A)
        
    def power(self, n):
        if n < 0:
            return None # raise exception?
        
        if n == 0:
            return identity(self.A.shape[0], format='coo')
        
        mat = copy.copy(self.A)
        for _ in range(1, n):
            mat = mat * self.A
        
        return mat
    