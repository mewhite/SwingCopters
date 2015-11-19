import random
import swing_copter
from swing_copter_constants import SC
from collections import Counter
from copy import deepcopy

class GamePlayer:
	actions = [True, False]
	def __init__(self, exploration_prob=0.1, step_size=.01, discount=.9):
		self.exploration_prob = exploration_prob
		self.weights = Counter()
		self.step_size = step_size
		self.discount = discount

	def extract_features_from_state(self, game_state):
		features = {}

		player = game_state.player
		walls = game_state.walls
		distance_to_wall = 0
		if walls:
			if player.acceleration > 0:
				right_wall = walls[1]
				distance_to_wall = right_wall.x - player.x
			else:
				left_wall = walls[0]
				distance_to_wall = player.x - left_wall.x + 354 # TODO: Change to reasonable (not 354)
		dtw = 0
		if distance_to_wall > 100:
			dtw = 1
		dtw2 = 0
		if dtw2 > 50:
			dtw2 = 1
		features["dtw"] = dtw
		features["dtw2"] = dtw2
		features["dtwn"] = -1 * dtw
		if player.acceleration > 0:
			distance_to_edge = SC.screen_width - player.x - player.width
		else:
			distance_to_edge = player.x
		dte200 = 0
		if distance_to_edge > 200:
			dte200 = 1
		dte100 = 0
		if distance_to_edge > 100:
			dte100 = 1
		features["distance_to_edge3"] = dte100
		features["distance_to_edge"] = dte200
		features["distance_to_edge2"] = -1 * dte200


		#self.weights["distance_to_edge"] = 1
		return features

	def estimate_state_score(self, game_state, action):
		next_state = deepcopy(game_state)
		next_state.update_state(action)
		features = self.extract_features_from_state(next_state)
		score = 0
		for feature, value in features.iteritems():
			score += value * self.weights[feature]
		print "state score for action: " + str(action) + " is " + str(score)
		return score

	def get_action(self, game_state):
		actions = GamePlayer.actions
		if random.random() < self.exploration_prob:
			return random.choice(actions)
		else:
			return max((self.estimate_state_score(game_state, action), action) for action in actions)[1]

	def normalize_weights(self):
		max_feature_weight = abs(self.weights.most_common(1)[0][1])
		if max_feature_weight > 0:
			for feature,value in self.weights.most_common():
				self.weights[feature] /= max_feature_weight

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
		#self.normalize_weights()