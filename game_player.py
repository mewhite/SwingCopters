import random
import swing_copter
from swing_copter_constants import SC
from collections import Counter
from copy import deepcopy

class GamePlayer:
	actions = [True, False]
	def __init__(self, exploration_prob=.1, step_size=.01, discount=1):
		self.exploration_prob = exploration_prob
		self.weights = Counter()
		self.step_size = step_size
		self.discount = discount

	def extract_features_from_state(self, game_state):
		features = {}

		player = game_state.player

		distance_to_edge = min(player.x, SC.screen_width - player.x - player.width)
		if distance_to_edge < 0:
			print "distance_to_edge: " + str(distance_to_edge)
			print "player feature stuff: " + str(SC.screen_width) + ", " + str(player.x) + ", " + str(player.width)

		features["distance_to_edge"] = distance_to_edge

		return features

	def estimate_state_score(self, game_state, action):
		next_state = deepcopy(game_state).update_state(action)
		features = self.extract_features_from_state(game_state)
		score = 0
		for feature, value in features.iteritems():
			score += value * self.weights[feature]
		return score

	def get_action(self, game_state):
		actions = GamePlayer.actions
		if random.random() < self.exploration_prob:
			return random.choice(actions)
		else:
			return max((self.estimate_state_score(game_state, action), action) for action in actions)[1]

	def incorporate_feedback(self, game_state, action, reward, next_game_state):
		actions = GamePlayer.actions
		prediction =  self.estimate_state_score(game_state, action)
		target = reward + (self.discount * max(self.estimate_state_score(next_game_state, next_action) for next_action in actions))
		residual = prediction - target
		if next_game_state.game_over:
			print "prediction: " + str(prediction)
			print "target: " + str(target)
			print "reward: " + str(reward)
			print "residual: " + str(residual)
		for feature, value in self.extract_features_from_state(game_state).iteritems():
			print "weights before: " + str(self.weights)
			print "feture value: " + str(value)
			self.weights[feature] -= self.step_size * residual * value
			print "weights after: " + str(self.weights)
