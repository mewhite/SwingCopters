# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 13:27:58 2015

@author: Nolan
"""

class StateTreeNode:
	def __init__(self, game_state, children=[None,None], parent=None, visits=0):
		self.children = children
		self.parent = parent
		self.visits = visits
		self.game_state = game_state