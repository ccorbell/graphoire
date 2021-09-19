#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 22:45:48 2021

@author: Christopher Corbell
"""

from graphoire.graph import Graph, vertexNeighborFromEdge
from graphoire.component import findComponents


def isCutVertex(vtx: int, G: Graph):
    return False

def findBlocks(G: Graph):
    
    blocks = []
    
    comps = findComponents(G)
    
    for comp in comps:
        if len(comp) == 1:
            # isolated vertices are blocks
            blocks.append(comp)
            continue
        
        # find blocks in this component
        
        exploredEdges = []
        visitedVertices = set()
        
        tree = {} # represented as dictionary of parent->immediate-child-list
        treeV = set() # set of vertices in tree
        
        activeVertex = comp[0]
        rootVertex = activeVertex
        
        while len(visitedVertices) < len(comp):
            neighbor = None
            unexploredEdge = None
            
            edges = G.getEdgesForVertex(activeVertex)
            for edge in edges:
                if not edge in exploredEdges:
                    unexploredEdge = edge
                    break
            
            if None != unexploredEdge:
                neighbor = vertexNeighborFromEdge(activeVertex, edge)
                exploredEdges.append(edge)
                    
                if not neighbor in treeV:
                    if not activeVertex in tree:
                        tree[activeVertex] = [neighbor]
                        activeVertex = neighbor
                    else:
                        tree[activeVertex].append(neighbor)
                    treeV.add(neighbor)
                
                        
                        
                
                
            
        
        
                
    return blocks


def findBlockWithVertex(vtx: int, G: Graph):
    block = []
    
    return block


