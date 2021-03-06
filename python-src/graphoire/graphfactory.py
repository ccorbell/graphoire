#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 10:07:28 2021

@author: Christopher Corbell
"""

from graphoire.graph import Graph
import copy
import random

class GraphFactory:
    def makeEmpty(n: int):
        """
        Return an empty Graph with n vertices.
        """
        return Graph(n)
    
    def makePath(n: int):
        """
        Return a path Graph with n vertices.
        """
        path = Graph(n)
        for i in range(0, n-1):
            #print(f"DEBUG - appending edge ({i}, {i+1})")
            path.edges.append([i, i+1])
        return path
    
    def makeCycle(n: int):
        """
        Return a cycle Graph with n vertices.
        """
        cycle = Graph(n)
        for i in range(0, n-1):
            #print(f"DEBUG - appending edge ({i}, {i+1})")
            cycle.edges.append([i, i+1])
            if i == 0:
                #print(f"DEBUG - appending edge (0, {n-1})")
                cycle.edges.append([0, n-1])        
        return cycle
    
    def makeComplete(n: int):
        """
        Return a complete Graph with n vertices.
        """
        complete = Graph(n)
        for i in range(0, n-1):
            for j in range(i+1, n):
                #print(f"DEBUG - appending edge ({i}, {j})")
                complete.edges.append([i, j])
        return complete
    
    def makeBipartiteComplete(m: int, n: int):
        """
        Return a complete bipartite Graph with m+n vertices.

        Parameters
        ----------
        m : int
            The size of the first partition.
        n : int
            The size of the second partition.
        """
        bip = Graph(m + n)
        for i in range(0, m):
            for j in range(m, m+n):
                #print(f"DEBUG - appending edge ({i}, {j})")
                bip.edges.append([i, j])
        return bip
        
    def makeKPartiteComplete(sizelist):
    	pass
    
    def makeHouse():
        """
        Return a 5-vertex 'house' Graph.
        """
        house = GraphFactory.makeCycle(5)
        house.addEdge(0, 2, True)
        return house
    
    def makeClaw():
        """
        Return a 4-vertex 'claw' Graph.
        """
        return GraphFactory.makeBipartiteComplete(3, 1)
    
    def makeBowtie():
        """
        Return a 5-vertex 'bowtie' Graph.
        """
        bowtie = GraphFactory.makeBipartiteComplete(3)
        bowtie.n = 5
        bowtie.addEdge(1, 3)
        bowtie.addEdge(1, 4)
        bowtie.addEdge(3, 4, True)
        return bowtie
    
    def makeKite():
        """
        Return a 4-vertex 'kite' Graph.
        """
        kite = GraphFactory.makeCycle(4)
        kite.addEdge(0, 2, True)
        return kite
        
    def makePetersen():
        """
        Return a 10-vertex Petersen Graph.
        """
        pet = GraphFactory.makeCycle(5)
        pet.n = 10

        secondCycle = []
        for edge in pet.edges:
            secondCycle.append([edge[0]+5, edge[1]+5])
        for edge in secondCycle:
            pet.edges.append(edge)
            
        pet.addEdge(0, 5)
        pet.addEdge(2, 6)
        pet.addEdge(4, 7)
        pet.addEdge(1, 8)
        pet.addEdge(3, 9)
        
        pet.sortEdges()
        
        return pet
        
    def makeRandomTree(n: int, maxDegree=0):
        usingMaxDegree = maxDegree >= 2
        
        tree = Graph(n)
        isolated_v_set = [item for item in range(0, n)]
        tree_v_set = []
        
        random.shuffle(isolated_v_set)
        
        # pick a vertex to start our tree from
        tree_v_set.append(isolated_v_set.pop())
        
        # now add leaves to the tree until it's done
        while len(isolated_v_set) > 0:
            nextLeaf = isolated_v_set.pop()
            leafNeighbor = random.choice(tree_v_set)
            
            tree.addEdge(nextLeaf, leafNeighbor, sortEdges=usingMaxDegree)
            tree_v_set.append(nextLeaf)
            
            if usingMaxDegree:
                deg = tree.vertexDegree(leafNeighbor)
                if deg >= maxDegree:
                    tree_v_set.remove(leafNeighbor)
        
        tree.sortEdges()
        return tree
        
        
    def makeGrotzsch():
        C5 = GraphFactory.makeCycle(5)
        return GraphFactory.makeMycielski(C5)
        
    def makeHarley(m: int, n: int):
        pass
    
    def makeHypercube(k: int, label=False):
        pass
    
    def makeMycielski(G: Graph):
        M = copy.copy(G)
        # Add n + 1 vertices (u's, and w)
        M.n = 2*G.n + 1
        
        # add edges from u to v-neighors
        for vi in range(0, G.n):
            ui = vi + G.n
            vNeighbors = G.getNeighbors(vi)
            for vN in vNeighbors:
                M.addEdge(ui, vN)
                
        w = M.n
        for ui in range(G.n, 2 * G.n):
            M.addEdge(ui, w)
        M.sortEdges()
        return M
        
    
    
    
    