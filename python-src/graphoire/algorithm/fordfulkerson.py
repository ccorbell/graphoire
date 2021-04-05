#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 09:39:29 2021

@author: mathaes
"""

import copy

from graphoire.labels import labelGraphVerticesWithIntegers
from graphoire.component import findComponents

class EdgeTolerance:
    def __init__(self, v1, v2, tol):
        self.v1 = v1
        self.v2 = v2
        self.tol = tol
        
    def __repr__(self):
        return f"EdgeTolerance .v1={self.v1} .v2={self.v2} .tol={self.tol}"
        
class FeasiblePath:
    def __init__(self):
        self.tolerance = -1
        self.vertices = []
        
    def __repr__(self):
        return f"FeasiblePath .tolerance={self.tolerance} .vertices={self.vertices}"
    
    def numEdges(self):
        return len(self.vertices) - 1
    
    def getPathEdge(self, index):
        if index >= 0 and index < len(self.vertices)-1:
            return [self.vertices[index], self.vertices[index+1]]
        return None
        
    def updateMinTolerance(self, tolerance):
        if self.tolerance < 0:
            self.tolerance = tolerance
        else:
            self.tolerance = min(self.tolerance, tolerance)
    
class FordFulkerson:
    def __init__(self, network):
        self.network = network
        self.edgeFlows = {}
        self.R = [network.source]
        self.S = []
        self.zeroEdgeFlows()
        self.enforceConstraints = False
        self.maxIterations = 1000
        
    def __repr__(self):
        s = "FordFulkerson\n"
        s += f".network:(\n  {self.network}\n)\n"
        s += f".edgeFlows: {self.edgeFlows}\n"
        return s
        
    def zeroEdgeFlows(self):
        self.edgeFlows = {}
        for edge in self.network.edges:
            self.edgeFlows[str(edge)] = 0
            
    def getEdgeFlow(self, tail, head):
        key = str([tail, head])
        if key in self.edgeFlows:
            return self.edgeFlows[key]
        else:
            print(f"WARNING: edge flow requested for unknown edge {key}")   
            return 0
    
    def setEdgeFlow(self, tail, head, flow):
        if flow < 0:
            flow = 0
            
        if self.enforceConstraints:
            # make sure we aren't setting a flow that exceeds capacity
            cap = self.getEdgeCapacity(tail, head)
            if flow > cap:
                raise Exception(f"Illegal flow {flow} on edge ({tail},{head}) exceeds capacity {cap}")
                
        key = str([tail, head])
        self.edgeFlows[key] = flow
        
    def addEdgeFlow(self, tail, head, value):
        """
        We are adding an available tolerance to an edge. Normally
        this is just added to the current edge flow. However if edge
        is reverse and has a positive flow, we subtract its current flow.
        """
        direction = self.network.edgeDirection(tail, head)
        if direction == 0:
            raise Exception(f"Logic error: attempt to add flow where there is no edge: {tail}->{head}")
        if direction > 0:
            flow = self.getEdgeFlow(tail, head)
            self.setEdgeFlow(tail, head, flow + value)
        else:
            flow = self.getEdgeFlow(head, tail)
            if flow <= 0:
                raise Exception(f"Logic error: attempt to reduce reversed-edge flow but it is <= 0: {head}->{tail}")
            if value > flow:
                raise Exception(f"Logic error: attempt to reduce reversed-edge flow by more than available: {head}->{tail}, current {flow}, value {value}")
            self.setEdgeFlow(head, tail, flow - value)
            
    def getEdgeCapacity(self, tail, head):
        return self.network.getEdgeCapacity(tail, head)
    
    def getEdgeTolerance(self, tail, head):
        return self.getEdgeCapacity(tail, head) - self.getEdgeFlow(tail, head)
            
    def getReverseEdgeTolerance(self, head, tail):
        # an in-flow has a tolerance equal to its
        # current flow (because we could 'push back' and reduce it to 0)
        return self.getEdgeFlow(tail, head)
    
    def run(self):
        iteration = 0
        foundMaxFlow = False
        while iteration < self.maxIterations:
            iteration += 1
            self.R = [self.network.source]
            self.S = []
            
            fpath = self.findAugmentingPath()
            if None == fpath:
                foundMaxFlow = True
                break
            else:
                # apply new path's tolerance to our flow
                for edgeIndex in range(0, fpath.numEdges()):
                    pathEdge = fpath.getPathEdge(edgeIndex)
                    self.addEdgeFlow(pathEdge[0], pathEdge[1], fpath.tolerance)

        if not foundMaxFlow:
            raise Exception(f"Failed to find maximum flow after {iteration} iterations")
            
        return foundMaxFlow
    
    def findAugmentingPath(self):
        
        availableEdgeTolerances = []
        reachedSink = False
        
        while len(self.R) > 0 and False == reachedSink:
            nextVertex = self.R.pop(0)
            if nextVertex in self.S:
                continue
            
            # Note as coded this is going to be breadth-first search
            
            adjacentTolerances = self.searchVertex(nextVertex)
            
            # note, nextVertex is now in S
            if len(adjacentTolerances) > 0:
                for adjVtx in adjacentTolerances:
                    edgeTol = EdgeTolerance(nextVertex, adjVtx, adjacentTolerances[adjVtx])
                    # save the edge vertices and tolerance found
                    availableEdgeTolerances.append(edgeTol)
                    
                    if adjVtx == self.network.sink:
                        reachedSink = True
                    
        if True == reachedSink:
            # form a path from our edges connected to sink
            fp = FeasiblePath()
            fp.vertices.insert(0, self.network.sink)
            
            while len(availableEdgeTolerances) > 0:
                nextEdgeTol = availableEdgeTolerances.pop()
                if nextEdgeTol.v2 == fp.vertices[0]:
                    
                    fp.updateMinTolerance(nextEdgeTol.tol)
                    fp.vertices.insert(0, nextEdgeTol.v1)
                    if nextEdgeTol.v1 == self.network.source:
                        break
                        
            return fp
        else:
            return None
                    
    def searchVertex(self, vtx):
        foundEdgeTolerances = {}
            
        outNeighbors = self.network.getOutNeighbors(vtx)
        for outNeighbor in outNeighbors:
            if not outNeighbor in self.S: # don't check searched vertices

                tol = self.getEdgeTolerance(vtx, outNeighbor)
                if tol > 0:
                    if not outNeighbor in self.R: 
                        self.R.append(outNeighbor) # mark as reached
                    foundEdgeTolerances[outNeighbor] = tol
        
        # also search for reverse-tolerances
        inNeighbors = self.network.getInNeighbors(vtx)
        for inNeighbor in inNeighbors:
            if not inNeighbor in self.S: # don't check searched vertices
                tol = self.getReverseEdgeTolerance(vtx, inNeighbor)
                if tol > 0:
                    if not inNeighbor in self.R: # mark as reached
                        self.R.append(inNeighbor)
                    foundEdgeTolerances[inNeighbor] = tol
        
        if vtx in self.S:
            print (f"ERROR: unexpected, searchVertex called on {vtx} which is already in S")
        else:
            self.S.append(vtx)
            
        return foundEdgeTolerances
     
    def findMinimumCutEdges(self):
        # Find earliest edges at full capacity when traversing from source
        tempR = [self.network.source]
        tempS = []
        
        cutEdges = []

        while len(tempR) > 0:
            vtx = tempR.pop()
            
            if vtx in tempS:
                continue # already searched
                
            outNeighbors = self.network.getOutNeighbors(vtx)
            for outNeighbor in outNeighbors:
                if not outNeighbor in tempS: # don't check searched vertices
                    tol = self.getEdgeTolerance(vtx, outNeighbor)
                    if tol == 0:
                        cutEdges.append([vtx, outNeighbor])
                    else:
                        tempR.append(outNeighbor)
            tempS.append(vtx)
        
        # remove any edges that have both vertices in tempS
        rmEdges = []
        for edge in cutEdges:
            if edge[0] in tempS and edge[1] in tempS:
                rmEdges.append(edge)
        
        for edge in rmEdges:
            cutEdges.remove(edge)
            
        return cutEdges
    
    def getTotalFlow(self):
        # total flow is calculated from inflows to sink
        flow = 0
        inNeighbors = self.network.getInNeighbors(self.network.sink)
        for inNeighbor in inNeighbors:
            flow += self.getEdgeFlow(inNeighbor, self.network.sink)        
        return flow
    
    
    def getMinimumCutFlow(self):
        
        cutEdges = self.findMinimumCutEdges()
        cutFlow = 0
        for cutEdge in cutEdges:
            cutFlow += self.getEdgeFlow(cutEdge[0], cutEdge[1])
        return cutFlow
        
        
        
    
        
        
        
        
        