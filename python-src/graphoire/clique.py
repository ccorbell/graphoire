#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 10:04:14 2021

@author: mathaes
"""
import itertools

from graphoire.graph import Graph
class SubClique:
    def __init__(self):
        self.vertices = set()
        
    def findMaximalSubcliques(G: Graph, 
                              vertex: int):
        """
        Starting from vertex in graph, find
        the maximal clique subgraph(s) that include
        vertex. Multiple subgraphs are returned if
        the vertex is involved in more than one clique
        of the same (maximal) size.

        Parameters
        ----------
        graph : A graphoire.Graph objects
            The graph.
        vertex : int
            The vertex to search for cliques.

        Returns
        -------
        A list of SubClique objects.

        """
        subcliques = []
        
        neighbors = G.getNeighbors(vertex)
        neighbors.sort() # so we build canonical edges from them
        neighborDegrees = {}
        for neighbor in neighbors:
            neighborDegrees[neighbor] = G.vertexDegree(neighbor)
            
        vDegree = len(neighbors)
        cliqueSize = vDegree + 1
        
        while cliqueSize > 0:
            cliqueCandidates = [vertex]
            for neighbor in neighbors:
                nDegree = neighborDegrees(neighbor)
                if nDegree >= cliqueSize - 1:
                    cliqueCandidates.append(neighbor)
                    
            if len(cliqueCandidates) < cliqueSize - 1:
                # can't have a clique of this size
                cliqueSize -= 1
                continue
            
            # it's possible we have a clique of cliqueSize
            # among the vertices of cliqueCandidates; we
            # must determine which if any actually form cliques
            # of this size.
            
            neighborEdges = []
            for neigbor in neighbors:
                others = G.getNeighbors(neighbor)
                for other in others:
                    if other == vertex or other in neighbors:
                        neighborEdges.append([neighbor, other])
            
            requiredEdgeCount = itertools.combinations(cliqueSize, 2)
            if len(neighborEdges) < requiredEdgeCount:
                # not enough mutual edges for a clique of this size
                continue
            elif len(neighborEdges) == requiredEdgeCount:
                if len(cliqueCandidates) == cliqueSize:
                    # singular clique match
                    sc = SubClique()
                    sc.vertices.update(cliqueCandidates)
                    subcliques.append(sc)
                else:
                    # we have at most one match, with the
                    # minimum number of edges but additional
                    # neighbor vertices - see if we can verify
                    # a single clique match  
                    pass
            else: 
                # len(neighborEdges) > requiredEdgeCount
                # ...we may have one or more matches - need
                # try all combinations of cliqueSize vertex sets
                # present in neighborEdges
                edgeVertexSet = set()
                for edge in neighborEdges:
                    edgeVertexSet.update(edge)
                
                
            