import numpy
from swing_copter import SwingCopters
from swing_copter_constants import SC

num_games = SC.mcts_num_games
print "MCTS max depth charge: " + str(SC.mcts_max_charge_depth)
print "MCTS number of charges: " + str(SC.mcts_num_charges)
print "MCTS number of games: " + str(num_games)
display_game = True
game = SwingCopters(display_game)
scores = game.run_mcts_player(num_games)
print "Scores: " + str(scores)
print "###############"
print "Test Settings:"
average_score =  sum(scores) / ( len(scores) + 0.0 )
print "Average Score: " + str(average_score)
st_dev = numpy.std(scores)
print "Standard Deviation: " + str(st_dev)
print "Max Score: " + str(max(scores))
print "Min Score: " + str(min(scores))
