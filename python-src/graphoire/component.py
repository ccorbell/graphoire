#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 11:28:27 2021

@author: Christopher Corbell
"""

from graphoire.graph import Graph

def isEulerian(G: Graph):
    """
    Return True if the graph is (undirected) Eulerian.
    """
    if G.n > 2 and isConnected(G):
        return G.isEven()
    return False

def isConnected(G: Graph):
    """
    Return True if the graph is connected.
    """
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

def verticesAreConnected(G: Graph, vertices):
    """
    Return true if the vertices indicated are connected by a path in G.
    
    Parameters
    ----------
    G : The Graph object.
    vertices : a list of vertex indices. E.g., provide two vertices if
      you want to test connection between any two points of the graph.

    Raises
    ------
    Exception if a vertex index is invalid / out-of-range.

    Returns
    -------
    True if all requested vertices are connected (in the same component).
    """
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
    """
    Find all the components of the Graph.

    Parameters
    ----------
    G : The graph

    Behavior:
        A component is represented as a list of vertex integer indices.
        (If you want the component's edges, you can query or use the
         inducedSubgraph method of the Graph with the given vertices.)
        This method returns a list of such components - so it is a list
        of (disjoint) lists of integers. An isolated vertex is represented as
        a list containing a single integer.
    Returns
    -------
    components : list of vertex-index component lists. Components are sorted ascending.
    """
    components = []
    visited = set()
    
    vCursor = 0
    
    while len(visited) < G.n:
        component = findComponentWithVertex(G, vCursor)
        #print(f"DEBUG - got component for vertex {vCursor}: {component}")
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
    """
    Determine and return the list of all vertices reachable from a vertex.

    Parameters
    ----------
    G : the Graph
    vertex : int
        The vertex index.

    Returns a list of vertex indices which are in the same component
    as the indicated vertex. The vertex-index-list is sorted ascending.
    
    Note this works the same for undirected and directed graphs,
    edge direction does not matter in determining component.
    """
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
