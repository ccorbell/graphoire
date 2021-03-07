#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 10:07:47 2021

@author: Christopher Corbell
"""

from graphoire.digraph import Digraph

class DigraphFactory:
    def makePath(n: int):
        path = Digraph(n)
        for i in range(0, n-1):
            path.edges.append((i, i+1))
        return path
    
    def makeCycle(n: int):
        cycle = Digraph(n)
        for i in range(0, n-1):
            cycle.edges.append((i, i+1))
        cycle.edges.append((n-1, 0))  
        return cycle
    
    def makeBipartiteComplete(n: int, m: int):
        bip = Digraph(n)
        
        for i in range(0, m):
            for j in range(m, m+n):
                #print(f"DEBUG - appending edge ({i}, {j})")
                bip.edges.append([i, j])
                bip.edges.append([j, i])
        bip.edges.sort()
        return bip
    