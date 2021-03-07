#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 10:07:28 2021

@author: Christopher Corbell
"""

from graphoire.graph import Graph

class GraphFactory:
    def makeEmpty(n: int):
        return Graph(n)
    
    def makePath(n: int):
        path = Graph(n)
        for i in range(0, n-1):
            #print(f"DEBUG - appending edge ({i}, {i+1})")
            path.edges.append([i, i+1])
        return path
    
    def makeCycle(n: int):
        cycle = Graph(n)
        for i in range(0, n-1):
            #print(f"DEBUG - appending edge ({i}, {i+1})")
            cycle.edges.append([i, i+1])
            if i == 0:
                #print(f"DEBUG - appending edge (0, {n-1})")
                cycle.edges.append([0, n-1])        
        return cycle
    
    def makeComplete(n: int):
        complete = Graph(n)
        for i in range(0, n-1):
            for j in range(i+1, n):
                #print(f"DEBUG - appending edge ({i}, {j})")
                complete.edges.append([i, j])
        return complete
    
    def makeBipartiteComplete(m: int, n: int):
        bip = Graph(m + n)
        for i in range(0, m):
            for j in range(m, m+n):
                #print(f"DEBUG - appending edge ({i}, {j})")
                bip.edges.append([i, j])
        return bip
        
    def makeKPartiteComplete(sizes: list[int]):
    	pass
    
    def makeHouse():
        house = GraphFactory.makeCycle(4)
        house.n = 5
        house.addEdge(0, 4)
        house.addEdge(1, 4)
        return house
    
    def makeClaw():
        claw = GraphFactory.makePath(3)
        claw.n = 4
        claw.addEdge(1, 3)
        return claw
    
    def makeBowtie():
        bowtie = GraphFactory.makeComplete(3)
        bowtie.n = 5
        bowtie.addEdge(1,3)
        bowtie.addEdge(1,4)
        return bowtie
    
    def makeKite():
        kite = GraphFactory.makeCycle(4)
        kite.addEdge(0, 2)
        return kite
        
    def makePetersen():
        pet = GraphFactory.makeCycle(5)
        pet.n = 10
        secondCycle = []
        for edge in pet.edges:
            secondCycle.append([edge[0]+5, edge[1]+5])
        for edge in secondCycle:
            pet.addEdge(edge)
            
        pet.addEdge(0, 5)
        pet.addEdge(2, 6)
        pet.addEdge(4, 7)
        pet.addEdge(1, 8)
        pet.addEdge(3, 9)
        
    def makeGrotzsch():
        pass
        
    def makeHarley(m: int, n: int):
        pass
    
    def makeHypercube(k: int, label=False):
        pass
    
    