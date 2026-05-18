#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 15:28:40 2021

@author: mathaes
"""

from graphoire.agent.graphmilieu import GraphMilieu

class PlanarMilieu(GraphMilieu):
    
    def __init__(self):
        GraphMilieu.__init__(self)
        self.plane = None
        