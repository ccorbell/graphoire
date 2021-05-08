#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 19:28:04 2021

@author: mathaes
"""

from graphoire.graph import Graph
import string

def makeIncrementingLabelsWithPrefix(prefix, count, start=0):
    labels = []
    
    for n in range(start, start+count):
        labels.append(prefix + str(n))
    return labels

def labelGraphVerticesWithAlphas(G: Graph, lowercase=True):
    """
    Assign alphabetic labels to the graph vertices. If there are more than
    26 vertices, a numeric suffix will be added, e.g. a1, b1, c1... a2, b2,
    etc.

    Parameters
    ----------
    G : Graph
        The graph to label.
    lowercase : bool, optional
        Whether to use lowercase or uppercase alphabetic characters.
        DESCRIPTION. The default is True (=lowercase)
        
    Note
    ----
    This will replace any existing vertex labels on the graph.
    """
    G.clearVertexLabels()
    
    alphas = string.ascii_lowercase
    if not lowercase:
        alphas = string.ascii_uppercase
    alpha_count = len(alphas)
    
    alpha_index = 0
    alpha_set = 1
    append_digit = G.order() > alpha_count
    
    for vertex in range(0, G.order()):
        label = alphas[alpha_index]
        if append_digit:
            label += str(alpha_set)
        G.setVertexLabel(vertex, label)
        alpha_index = (alpha_index + 1) % alpha_count
        if 0 == alpha_index:
            alpha_set += 1
            
def labelGraphVerticesWithIntegers(G: Graph, addValue=0):
    """
    Assign integer (type int) labels to the graph vertices, based on current
    vertex indices. 

    Parameters
    ----------
    G : Graph
        The graph to label.
    addValue: int, optional
        A value to add to each index for labeling. E.g. adding 100 will
        label vertices 100, 101, 102. Adding 1 will apply
        one-based labels instead of zero-based. The default value is 0.
        
    Behavior
    --------
    This applies labels to each vertex based on its zero-based
    vertex index, plus any addValue supplied. 
    
    Note that labels *can* then become different from underlying indices, 
    for example if vertices are deleted, if labels are transferred to an
    induced supgraph, etc. Call this function again with a graph to re-apply
    labels that match the graph's contiguous indices.
    """
    G.clearVertexLabels()
    
    for vertex in range(0, G.order()):
        labelInt = vertex + addValue
        G.setVertexLabel(vertex, labelInt)
    
def labelGraphVerticesWithIntegerStrings(G: Graph, addValue=0):
    """
    Assign integer-string labels to the graph vertices, based on current
    vertex indices. 

    Parameters
    ----------
    G : Graph
        The graph to label.
    addValue: int, optional
        A value to add to each index for labeling. E.g. adding 100 will
        label vertices '100', '101', '102'. Adding one will apply
        one-based labels instead of zero-based. The default value is 0.
        
    Behavior
    --------
    This applies labels to each vertex based on its zero-based
    vertex index, plus any addValue supplied. 
    
    Note that labels *can* then become different from underlying indices, 
    for example if vertices are deleted, if labels are transferred to an
    induced supgraph, etc. Call this function again with a graph to re-apply
    labels that match the graph's contiguous indices.
    """
    G.clearVertexLabels()
    
    for vertex in range(0, G.order()):
        labelInt = vertex + addValue
        G.setVertexLabel(vertex, str(labelInt))
    