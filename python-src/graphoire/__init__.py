#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 10:22:57 2021

@author: mathaes
"""
__all__ = ["graph", "graphfactory", "digraph", "digraphfactory", "component", "graph2matrix", "labels", "prufer", "tree" "matrixfactory"]
from graphoire.graph import Graph
from graphoire.graphfactory import GraphFactory

from graphoire.digraph import Digraph
from graphoire.digraphfactory import DigraphFactory

from graphoire.component import *

from graphoire.graph2matrix import *

from graphoire.labels import *
from graphoire.prufer import *
from graphoire.tree import *

from graphoire.matrixfactory import MatrixFactory

"""
Things that would be interesting to implement:
    - determine if an edge is a cut edge
    - determine if a vertex is a cut vertex
    - determine if a vertex belongs to a cycle
    - determine if an edge belongs to a cycle
    - determine if a connected graph is bipartite
    - generally, find cycles within a connected graph
    - generally, determine if a graph is acyclic
    - form an sum or disjoint union of two graphs
    - form a vertex-merging union (aka composition) of two graphs
    - apply Havel-Hakimi to a degree sequence
    - find the kernel of a digraph
    - find cycles / odd cycles in a digraph
    - get adjacency matrix of a digraph
    - get incidence and edge matrices of a digraph
    - get in-neighborhood and out-neighborhood of a digraph
    - form the bipartite split of a diagraph
    - determine if a digraph has a Eulerian circuit
    - create a DeBruijn graph with symbolic labels
    - efficiently find all leaves in an acyclic (or other) graph
    - find minimum-length path from u to v
    - return distance from u to v (length of min-length path)
    - find diameter of G
    - find eccentricity of vertex in G
    - find radius (min eccentricity) of G
    - find center of G (induced on vertices of min eccentricity)
    - find the Wiener index of a graph
    - 
"""