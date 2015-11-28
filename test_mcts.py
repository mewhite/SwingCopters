import mcts
from game_state import GameState
from player import Player
from swing_copter_constants import SC
from collections import deque

player = Player(SC.player_start_pos, 0, 0)
walls = deque()
hammers = deque()
game_state = GameState(player, walls, hammers, 0, False)

print mcts.get_MCTS_action(game_state)