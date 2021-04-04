#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 10:19:23 2021

@author: mathaes
"""
import numpy as np
from scipy.sparse import coo_matrix

class MatrixFactory:
    
    # make cycle adjacency matrix
    
    def makeCycleAdjM_dense(n: int):
        g = np.zeros((n, n), dtype=int)
    
        j = -1
        for i in range(0, n):
            g[i][j % n] = 1
            g[i][(j+2) % n] = 1
            j += 1
        return g
    
    def makeCycleAdjM_sparse_coo(n: int):
        rows = np.array()
        cols = np.array()
        values = np.array()
        
        j = -1
        for i in range(0, n):
            rows.append(i)
            cols.append(j%n)
            values.append(1)
            
            rows.append(i)
            cols.append((j+2) % n)
            values.append(1)
            
            j += 1
            
        return coo_matrix((values, (rows, cols)), shape=(n, n), dtype=int)
    
    def makeCycleAdjM_sparse_csr(n: int):
        return MatrixFactory.makeCycleAdjM_sparse_coo(n).tocsr()
    
    # make complete-graph adjacency matrix
    
    def makeCompleteAdjM_dense(n: int):
        g = np.ones((n, n), dtype=int)
        for i in range(0, n):
            g[i][i] = 0
        return g
    
    def makeCompleteAdjM_sparse_coo(n: int):
        # might as well start with dense for a complete graph
        return coo_matrix(MatrixFactory.makeCompleteAdjM_dense())
    
    def makeCompleteAdjM_sparse_csr(n: int):
        return MatrixFactory.makeCycleAdjM_sparse_coo().tocsr()
    
    # make path adjacency matrix
    
    def makePathAdjM_dense(n: int):
        g = np.zeros((n, n), dtype=int)
    
        g[0][1] = 1
        j = 0
        for i in range(1, n-1):
            g[i][j] = 1
            g[i][(j+2) % n] = 1
            j += 1
        g[n-1][n-2] = 1
        return g
    
    def makePathAdjM_sparse_coo(n: int):
        rows = np.array()
        cols = np.array()
        values = np.array()
        
        rows.append(0)
        cols.append(1)
        values.append(1)
        
        j = 0
        for i in range(1, n-1):
            rows.append(i)
            cols.append(j)
            values.append(1)
            
            rows.append(i)
            cols.append((j+2)%n)
            values.append(1)

            j += 1
        rows.append(n-1)
        cols.append(n-1)
        values.append(1)
        return coo_matrix((values, (rows, cols)), shape=(n, n), dtype=int)
    
    def makePathAdjM_sparse_csr(n: int):
        return MatrixFactory.makePathAdjM_sparse_coo(n).tocsr()
        
    
    # make regular adjacency matrix
    
    def makeRegularAdjM_dense(n: int, d: int):
        if d > n-1:
            raise Exception("Graph error: vertex degree cannot exceed n-1")
            
        if n % 2 ==1 and d % 2 == 1:
            raise Exception("Graph error: cannot construct an odd number of vertices with all odd degrees")
            
        raise Exception("makeRegularAdjM_dense not yet implemented")
    
    def makeRegularAdjM_sparse_coo(n: int, d: int):
        if d > n-1:
            raise Exception("Graph error: vertex degree cannot exceed n-1")
            
        if n % 2 ==1 and d % 2 == 1:
            raise Exception("Graph error: cannot construct an odd number of vertices with all odd degrees")
            
        raise Exception("makeRegularAdjM_dense not yet implemented")
        
    def makeRegularAdjM_sparse_csr(n: int, d: int):
        return MatrixFactory.makeRegularAdjM_sparse_coo(n).tocsr()
        
    # make bipartite complete adjacency matrix
    
    def makeBipartiteCompleteAdjM_dense(m: int, n: int):
        g = np.zeros((m+n, m+n), dtype=int)
        for i in range(0, m):
            for j in range(m, m+n):
                g[i][j] = 1
                g[j][i] = 1
        return g
    
    def makeBipartiteCompleteAdjM_sparse_coo(m: int, n: int):
        rows = np.array()
        cols = np.array()
        values = np.array()
        
        for i in range(0, m):
            for j in range(m, m+n):
                rows.append(i)
                cols.append(i)
                values.append(1)
                
        for i in range(m, m+n):   
            for j in range(0, m):
                rows.append(i)
                cols.append(i)
                values.append(1)
                
        return coo_matrix((values, (rows, cols)), shape=(m+n, m+n), dtype=int)
        
    def makeBipartiteCompleteAdjM_sparse_coo(m: int, n: int):
        return MatrixFactory.makeBipartiteCompleteAdjM_sparse_coo(n).tocsr()

        
    # make petersen graph adjacency matrix
    
    def makePertersenAdjM_dense():
        array = np.zeros((10, 10))
        pass


