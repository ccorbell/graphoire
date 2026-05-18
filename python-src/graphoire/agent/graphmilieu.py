#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 15:28:31 2021

@author: mathaes
"""

from graphoire.agent.milieu import Milieu

class GraphMilieu(Milieu):
    
    def __init__(self):
        Milieu.__init__(self)
        self.graph = None
        
    def getRandomVertexAgent(self):
        pass
    
    def getUnrelatedVertexAgent(self, agent):
        pass
    
    