#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 15:23:30 2021

@author: mathaes
"""

from graphoire.agent.agent import Agent

class VertexAgent(Agent):
    
    def __init__(self, vertex: int, milieu):
        self.vertex = vertex
        self.milieu = milieu
        
        self.useEdgeBehavior = False
        self.usePlanarBehavior = False
        
        # edge behavior fields
        self.currentDegree = 0
        self.stableDegree = 0
        self.desiredDegree = 0
        self.maxDegree = 0
        
    def iterate(self):
        # apply behaviors
        
        if self.useEdgeBehavior:
            self.applyEdgeBehavior()
            
        if not None == self.planarBehavior:
            self.applyPlanarBehavior()
            
    def isStable(self):
        stable = True
        
        self.currentDegree = self.milieu.graph.getVertexDegree(self.vertex)
        
        if self.useEdgeBehavior:
            stable = self.currentDegree >= self.stableDegree
            
        # TODO also check planar stability if enabled
        return stable
            
    def applyEdgeBehavior(self):
        G = self.milieu.graph
        self.currentDegree = G.getVertexDegree(self.vertex)
        if self.currentDegree < self.desiredDegree:
            self.proposeEdge()
    
    def proposeEdge(self):
        # find a vertex agent in the miliue
        candidate = self.mileu.getUnrelatedVertexAgent(self)
        if candidate.handleEdgeProposal():
            self.milieu.graph.addEdge(self.vertex, candidate.vertex, True)
            self.currentDegree = self.milieu.graph.getVertexDegree(self.vertex)
            
    # TODO: add optional methods for agent to locate its preferred
    # candidate for edge proposal, rather than relying on
    # milieu implementations
    
    def handleEdgeProposal(self, proposer):
        """
        Respond to proposal to establish an edge with proposer vertex-agent.

        Parameters
        ----------
        proposer : VertexAgent
            The other vertex agent.

        Returns
        -------
        True if the edge proposal is accepted, False if rejected.

        """
        if self.currentDegree >= self.maxDegree:
            return False
        
        if self.currentDegree >= self.desiredDegree:
            # acceptance is randomized, probability lower 
            # the further above desired degree we get
            probability = 0.5
            maxDesiredDelta = self.maxDegree - self.desiredDegree
            
            
            
        return True
    
    
    def applyPlanarBehavior(self):
        pass
        