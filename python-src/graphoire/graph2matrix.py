#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 18:50:04 2021

@author: mathaes
"""

import numpy as np
from scipy.sparse import coo_matrix

from graphoire.graph import Graph

def graphToAdjacencyMatrix(G: Graph):
        """
        Returns an adjacency matrix for Graph, as a scipy.sparse.coo_matrix
        """
        iList = []
        jList = []
        
        i = 0
        j = 0
        for i in range(0, G.order()):
            for j in range(i+1, G.order()):
                if G.hasEdge(i, j):
                    iList.append(i)
                    jList.append(j)
                    
                    iList.append(j)
                    jList.append(i)
        
        return coo_matrix((np.ones(len(iList), dtype=int), (iList, jList)), shape=(G.order(), G.order()))
        
def adjacencyMatrixToGraph(A):
    """
    Returns a Graph object constructed from adjacency matrix A

    Parameters
    ----------
    A : scipy.sparse.coo_matrix
        An adjacency matrix in sparse coordinate format.
    """
    # TODO: support input as CSR, CSC
    G = Graph(A.shape[0])
    for nnz in range(0, len(A.row)):
        i = A.row[nnz]
        j = A.col[nnz]
        if i < j:
            G.addEdge(i, j)
    G.sortEdges() # just in case sparse data wasn't sorted
    return G

    
def graphToEdgeVertexMatrix(G: Graph):
    """
    Returns an edge-vertex matrix for Graph (rows=edges, columns=vertices), as a scipy.sparse.coo_matrix.
    """
    iList = []
    jList = []
    for ei in range(0, len(G.edges)):
        edge = G.edges[ei]
        iList.append(ei)
        jList.append(edge[0])
        iList.append(ei)
        jList.append(edge[1])
    return coo_matrix((np.ones(len(iList), dtype=int), (iList, jList)), shape=(G.edgeCount(), G.order()))
    
def graphToIncidenceMatrix(G: Graph):
    """
    Returns an incidence matrix for Graph (rows=vertices, columns=edges), as a scipy.sparse.coo_matrix
    """
    return graphEdgeVertexMatrix().transpose()

