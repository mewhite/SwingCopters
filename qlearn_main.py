from swing_copter import SwingCopters
from swing_copter_constants import SC
import numpy

display_game = True
game = SwingCopters(display_game)
num_games = 20
scores = game.run_qlearning_player(num_games)

print "Scores: " + str(scores)
print "###############"
print "Test Settings:"
average_score =  sum(scores) / ( len(scores) + 0.0 )
print "Average Score: " + str(average_score)
st_dev = numpy.std(scores)
print "Standard Deviation: " + str(st_dev)
print "Max Score: " + str(max(scores))
print "Min Score: " + str(min(scores))
