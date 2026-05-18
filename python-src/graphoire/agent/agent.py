#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 12:16:05 2021

@author: mathaes
"""

class Action:
    def run(self, agent, milieu):
        return None
    
class Agent:
    def __init__(self):
        self.actions = []
        
    def observe(self, milieu):
        pass
    
    def selectAction(self):
        return None
    
    def run1(self, milieu):
        result = None
        
        self.observe(milieu)
        action = self.selectAction()
        if None != action:
            result = action.run(self, milieu)
        return result
    
    def runN(self, milieu, n):
        for i in range(0, n):
            result = self.run1(milieu)
            if None == result:
                return i+1
        return n