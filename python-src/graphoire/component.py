#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 11:28:27 2021

@author: Christopher Corbell
"""

from graphoire.graph import Graph

def isEulerian(G: Graph):
    if G.n > 2 and isConnected(G):
        return G.isEven()
    return False

def isConnected(G: Graph):
    # fast check on number of edges
    if len(G.edges) < G.n - 1:
        # not possible to be connected
        return False
    
    # get the component for the first vertex
    comp0 = findComponentWithVertex(G, 0)
    
    # If this component is smaller than G, some
    # vertex is not connected to v=0, so the graph
    # is not connected
    return len(comp0) == G.n

def isConnectedAcyclic(G: Graph):
    return gwIsConnected(G) and len(G.edges) == G.n - 1

def verticesAreConnected(G: Graph, vertices):
    comps = findComponents(G)
    vertexNotFound = True
    for comp in comps:
        if vertices[0] in comp:
            for vi in range(1, len(vertices)):
                if not vertices[vi] in comp:
                    return False
            # all vertices are in same component
            return True
    if vertexNotFound:
        # if we get here's there's an input error
        raise Exception(f"Bad vertex parameter - vertex {vertices[0]} not in any component")
    
def findComponents(G: Graph):
    components = []
    visited = set()
    
    vCursor = 0
    
    while len(visited) < G.n:
        component = findComponentWithVertex(G, vCursor)
        print(f"DEBUG - got component for vertex {vCursor}: {component}")
        components.append(component)
        for v in component:
            visited.add(v)
        
        if len(visited) < G.n:
            # find next unused vertex index
            for vNext in range(0, G.n):
                if vNext in visited:
                    continue
                vCursor = vNext
                #print(f"DEBUG - checking {vCursor} next loop...")
                break
            if vNext >= G.n:
            	# raise exception?
                print("UNEXPECTED: could not find available vertex from loop")
                
    return components
        
def findComponentWithVertex(G: Graph, vertex: int):
    componentSet = set()
    componentSet.add(vertex)
    
    unprocessedVertices = set()
    unprocessedVertices.add(vertex)
    while len(unprocessedVertices) > 0:
        nextVertex = unprocessedVertices.pop()
        edges = G.getEdgesForVertex(nextVertex)
        for edge in edges:
            if not edge[0] in componentSet:
                componentSet.add(edge[0])
                unprocessedVertices.add(edge[0])
                
            if not edge[1] in componentSet:
                componentSet.add(edge[1])
                unprocessedVertices.add(edge[1])
                
    result = list(componentSet)
    result.sort()
    return result
