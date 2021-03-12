#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 09:43:18 2021

@author: Christopher Corbell

PrefsGraph is a bipartite-complete Digraph with weighted edges
representing preferences.

Each partition is equivalent to one side of a preference
matching graph for a stable-matching algorithm like
Gale-Shapley.

"""

from graphoire.digraph import Digraph

class PrefsGraph(Digraph):
    def __init__(self, n: int):
        Digraph.__init__(self, n)
        


