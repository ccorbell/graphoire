#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 10:07:28 2021

@author: Christopher Corbell
"""

from graphoire.graph import Graph
from graphoire.labels import labelGraphVerticesWithBinaryStrings, binaryStringDigitDiff

import copy
import random
import math
import itertools

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
        
    def makeKPartiteComplete(partitionSizes):
        order = sum(partitionSizes)
        g = Graph(order)
        
        headCursor = 0
        
        for current_block in range(0, len(partitionSizes)):
            current_block_size = partitionSizes[current_block]
            for head in range(headCursor, headCursor + current_block_size):
                tailCursor = 0
                for tailBlock in range(0, len(partitionSizes)):
                    blockSize = partitionSizes[tailBlock]
                    
                    if tailBlock == current_block:
                        # skip all targets in current block
                        tailCursor += blockSize
                        continue
                    else:
                        for tail in range(tailCursor, tailCursor + blockSize):
                            g.addEdge(head, tail)
                        tailCursor += blockSize
                        
            headCursor += current_block_size
            
        return g
            
    
    def makeTuranGraph(order, r):
        """
        Create a Turan graph, i.e., a multipartite
        complete graph on n vertices with r partitions.

        Parameters
        ----------
        order : int
            The total number of vertices.
        r : int
            The number of partitions.

        Returns
        -------
        A Graph object.

        """
        if r > order:
            raise Exception("ERROR, makeTuranGraph requires order > r")
            
        sizeList = []
        
        rem = order % r
        if 0 == rem:
            sizeList = [int(order / r)] * r
        else:
        
            avg = order / r
            l_size = int(math.floor(avg))
            u_size = l_size + 1
            u_count = order - (l_size * r)
            l_count = r - u_count
            
            sizeList = [l_size] * l_count
            sizeList += [u_size] * u_count
        
        return GraphFactory.makeKPartiteComplete(sizeList)
        
    
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
        return GraphFactory.makeKSubsetExclusionGraph(5, 2)
    
    def deprecated_makePetersen():
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
    
    def makeKSubsetExclusionGraph(n, k):
        """
        Considering the integer set [n], create vertices corresponding to
        and labeled with every possible k-subset of [n], and
        add an edge only between vertices whose subset-labels
        are disjoint.
        
        Note that makeKSubsetExclusionGraph(5, 2) will
        generate the Petersen graph, so this function can
        be used to generate Petersen-like graphs based on
        different n-sizes and subset sizes.
        

        Parameters
        ----------
        n : int
            The maximum integer for the [n] set used; note this is not
            the graph order
        k : int
            The size of subsets of [n] to use for vertex labels and 
            edge-creation.

        Returns
        -------
        A graph with the indicated properties, including labels corresponding
        to subsets.
        """
        order = math.comb(n, k)
        #print (f"order is {order}")
        
        g = Graph(order)
        
        nset = list(range(1, n+1))
        isubs = itertools.combinations(nset, k)
        sublabels = list(isubs)
        if len(sublabels) != order:
            raise Exception(f"Unexpected combination count {len(sublabels)} for order {order}, n={n}, k={k}")
                
        for vertex in range(0, order):
            g.setVertexLabel(vertex, sublabels[vertex])
            
        for head in range(0, order):
            headLabel = g.getVertexLabel(head)
            
            for tail in range(0, order):
                if tail == head:
                    continue
                tailLabel = g.getVertexLabel(tail)
                if len(set(headLabel) & set(tailLabel)) == 0:
                    #print(f"Adding edge from {head} to {tail}, labels {headLabel}, {tailLabel}")
                    g.addEdge(head, tail)
                    
        return g
        
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
    
    def makeHypercube(exponent: int, label=False):
        """
        Make the hypercube Q_(exponent), i.e., 
        with order 2^(exponent)

        Parameters
        ----------
        exponent : int (non-negative)
            The power of 2, or subscript of Q, for the hypercube.

        Returns
        -------
        A Graph object (the hypercube graph), with optional binary-string vertex labels

        """
        
        if exponent < 0:
            raise Exception("")
        order = 2**exponent
        hypercube = Graph(order)
        if order == 1:
            return hypercube

        for head in range(0, order - 1):
            for tail in range(head, order):
                xor = head ^ tail
                # if xor is a power of 2, these values differ in 1 bit
                if xor and (not(xor & (xor - 1))):
                    hypercube.addEdge(head, tail)

    
        # we use the binary-label approach to add edges, and return
        # a graph with labels
        if True == label:
            labelGraphVerticesWithBinaryStrings(hypercube, exponent)
                    
        return hypercube
        
    
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
        
    
    
    
    