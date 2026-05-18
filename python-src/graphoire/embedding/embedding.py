#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 09:15:01 2021

@author: mathaes
"""

from graphoire.graph import Graph

class Embedding:
    """
    An Embedding object represents a graph embedding into some
    coordinate system or similar environment. This base class
    does not enforce any particular coordinate system; see
    subclasses PlanarEmbedding and CubicEmbedding for 2-D and 3-D
    cartesian embeddings.
    
    An embedding assigns a location to each vertex, and may also
    assign a curve to some or all edges; if the latter is omitted the edge
    embedding is assumed to be a line segment between vertex locations.
    """
    
    def __init__(self, graph: Graph):
        self.graph = graph
        self.vertexLocations = {}
        self.edgeCurves = {}
        
    def getVertexLocation(self, vertex):
        """
        Get the location of a vertex

        Parameters
        ----------
        vertex : int
            The vertex index.

        Returns
        -------
        location
            A location, typically a tuple of values representing a coordinate
            in some coordinate system, though it could also be a single 
            value (e.g. in a line-embedded graph) or an object
            
            Returns None if no location has been set for the vertex.

        """
        if vertex in self.vertexLocation:
            return self.vertexLocations[vertex]
        return None
    
    def setVertexLocation(self, vertex, location):
        """
        Set a vertex location

        Parameters
        ----------
        vertex : int
            The vertex index.
        location : object
            The location of the vertex in the embedding. For planar embeddings
            this should be a tuple of two values; for 3-D embeddings it
            will have three values. Other embeddings may use custom objects
            or scalar values instead of tuples.

        Returns
        -------
        None.

        """
        self.vertexLocations[vertex] = location
        
    def getEdgeCurve(self, edge):
        """
        Get the curve for the embedded edge

        Parameters
        ----------
        edge : list or tuple
            The edge should contain two integer values (vertex indices),
            which should be valid indices for the embedded graph.

        Returns
        -------
            An tuple representing an the edge as a Bézier curve
            between the embedded points of the vertices; if no curve
            has been set, it will be a line segment. This function may
            return None if the vertices are invalid or do not yet have
            embedded locations.
        """
        result = None
        if edge in self.edgeCurves:
            result = self.edgeCurve[edge]
        else:
            loc1 = self.getVertexLocation(edge[0])
            loc2 = self.getVertexLocation(edge[1])
            if not (None == loc1 or None == loc2):
                result = (loc1, loc2)
        return result
    
    def setEdgeCurve(self, edge, curve):
        """
        

        Parameters
        ----------
        edge : list or tuple
            The edge should include two values, the head and tail vertex
            indices (as integers)
        curve : list or tuple, or None
            The curve is a list of points interpreted as a Bézier curve.
            The start and end points should be the same as the embedding's
            vertex location for the edge endpoints.
            
            If None is supplied, any set value is removed and the default
            (line segment) will be returned for this curve.

        Returns
        -------
        None.

        """
        self.edgeCurves[edge] = curve
        
