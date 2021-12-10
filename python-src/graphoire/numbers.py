#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 23 10:41:14 2021

@author: mathaes
"""

"""
graphoire.numbers contains constants and numeric/combinatorial forumulas 
that are useful for graph theory. 

Many of these are synonyms that can be used to make particular logic
more expressive / semantic.

Simple stateless functions are included here, more complex algorithms
will be in graphoire.algorithm or graphoire.linalg.
"""

def maximum_path_length(num_vertices):
    return num_vertices - 1

def minimum_connected_edge_count(num_vertices):
    return maximum_path_length(num_vertices)

def arithmetic_sum(n):
    value = 0
    for term in range(1, n):
        value += term
    return value
    
def n_choose_2(n):
    return arithmetic_sum(n)

def complete_graph_size(num_vertices):
    return n_choose_2(num_vertices - 1)



