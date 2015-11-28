# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 13:27:58 2015

@author: Nolan
"""

class StateTreeNode:
	def __init__(self, game_state, utility=0, parent=None, visits=0):
		self.utility = utility
		self.children = [None, None]
		self.parent = parent
		self.visits = visits
		self.game_state = game_state