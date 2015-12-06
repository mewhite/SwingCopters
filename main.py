# -*- coding: utf-8 -*-
"""
Created on Sun Nov 01 18:02:00 2015

@author: Nolan
"""

from swing_copter import SwingCopters
from swing_copter_constants import SC

print "MCTS max depth charge: " + str(SC.mcts_max_charge_depth)
print "MCTS number of charges: " + str(SC.mcts_num_charges)
display_game = False
game = SwingCopters(display_game)
num_games = 20
scores = game.run_mcts_player(num_games)
print "Scores: " + str(scores)
print "Test Settings:"

average_score =  sum(scores) / ( len(scores) + 0.0 )
print "Average Score: " + str(average_score)
st_dev = sum([(scores[i] - average_score) for i in range(len(scores))]) / (len(scores) + 0.0)
print "Standard Deviation: " + str(st_dev)
print "Max Score: " + str(max(scores))
print "Min Score: " + str(min(scores))
