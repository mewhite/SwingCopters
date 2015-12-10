from swing_copter import SwingCopters
from swing_copter_constants import SC

display_game = True
game = SwingCopters(display_game)
scores = game.run_human_player(num_games = 10)
average_score =  sum(scores) / ( len(scores) + 0.0 )
print "Average score: " + str(average_score)