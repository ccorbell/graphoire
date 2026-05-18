#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 09:42:25 2021

@author: mathaes
"""

from graphoire.embedding import Embedding

class PlanarEmbedding(Embedding):
    def __init__(self, graph):
        Embedding.__init__(self, graph)
        
    
    