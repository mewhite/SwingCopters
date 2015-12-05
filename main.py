# -*- coding: utf-8 -*-
"""
Created on Sun Nov 01 18:02:00 2015

@author: Nolan
"""

from swing_copter import SwingCopters

display_game = False
game = SwingCopters(display_game)
#game.run_human_player()
num_games = 20
scores = game.run_mcts_player(num_games)
print "Scores: " + str(scores)
print "Average Score: " + str(sum(scores) / ( len(scores) + 0.0 ))