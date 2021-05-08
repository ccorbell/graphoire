#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 14:17:47 2021

@author: mathaes
"""

from graphoire.graph import Graph

class DFSTreeVisitor:
    def __init__(self):
        self.stopSearch = False
        self.nextVertex = None
        
    def visit(self, G: Graph, vertex, neighbors):
        # override to change this selection behavior or
        # to implement conditions to stop the search
        if None != neighbors and len(neighbors) > 0:
            self.nextVertex = neighbors[0]
        else:
            self.nextVertex = None
        
def dfstree(G: Graph, start=None, visitor=None, verbose=False):
    """
    The defstree method does a depth-first search to find a spanning
    tree of the graph G starting at the indicated start vertex. 
    The spanning tree is returned as a set of edges.
    
    Note that if G is not connected then the returned tree will only
    span the component which contains the start vertex.
    
    An optional visitor object can be passed in. Its visit()
    method is invoked each time a new vertex is visited. The visitor
    make set a stop flag to signal the algorithm to stop and exit.
    The visitor may also indicate which unvisited neighbor to
    search next. If visitor is omitted, the

    Parameters
    ----------
    G : Graph
        DESCRIPTION.
    start : int, optional
        The vertex from which to start. The default is 0.
    visitor : DFSTreeVisitor, optional
        The visitor to invoke during tree search. The default is None; a local DFSTreeVisitor() will be used.

    Returns
    -------
    Edges, as a list of edge-lists, with each edge-list containing two vertex integer values.

    """
    if None == start:
        start = 0
    if None == visitor:
        visitor = DFSTreeVisitor()
        
    searchComplete = False
    searchInterrupt = False
    edges = []
    
    visitedVertices = []
    skippedNeighbors = {}
    
    currentVertex = start
    
    
    while not searchComplete and not searchInterrupt:
        if verbose:
            print (f"currentVertex: {currentVertex}")
        allNeighbors = G.getNeighbors(currentVertex)
        
        unexploredNeighbors = []
        for neighbor in allNeighbors:
            if not neighbor in visitedVertices:
                unexploredNeighbors.append(neighbor)
                
        nextNeighbor = None
        if len(unexploredNeighbors) > 0:
            
            visitor.visit(G, currentVertex, unexploredNeighbors)
            visitedVertices.append(currentVertex)
            if currentVertex in skippedNeighbors:
                skippedNeighbors.pop(currentVertex)
                
            searchInterrupt = visitor.stopSearch
            nextNeighbor = visitor.nextVertex

            if not searchInterrupt:
                for unexplored in unexploredNeighbors:
                    if unexplored != nextNeighbor:
                        if not unexplored in skippedNeighbors:
                            skippedEdge = [currentVertex, unexplored]
                            skippedNeighbors[unexplored] = skippedEdge
        else:
            if verbose:
                print (" - no unexplored neighbors")
            visitedVertices.append(currentVertex)
            
        if searchInterrupt:
            break
        
        if None == nextNeighbor:
            if len(skippedNeighbors) > 0:
                item = skippedNeighbors.popitem()
                if verbose:
                    print (f" - going back to unexplored edge {item[1]} for neighbor {item[0]}")
                currentVertex = item[1][0]    
            else:
                currentVertex = None
        else:
            nextEdge = [currentVertex, nextNeighbor]
            nextEdge.sort()
            if verbose:
                print(f"appending edge {nextEdge}")
            if nextEdge in edges:
                print ("ERROR: edge is already in results!")
                break
            
            edges.append(nextEdge)
            currentVertex = nextNeighbor 
            
        if None == currentVertex:
            searchComplete = True

    return edges
