import random
import swing_copter
from swing_copter_constants import SC
from collections import Counter
from copy import deepcopy

#Q learning game player
class QLearningPlayer:
	actions = [True, False]
	def __init__(self, exploration_prob=0.1, step_size=.01, discount=.75):
		self.exploration_prob = exploration_prob
		self.weights = Counter()
		self.step_size = step_size
		self.discount = discount

	def add_discrete_features(self, value, feature_name, start, end, increment):
		temp_name = feature_name + "_-"
		if value < start:
			self.features[temp_name] = 1
		else:
			self.features[temp_name] = 0

		temp_name = feature_name + "_+"
		if value > end:
			features[temp_name] = 1
		else:
			self.features[temp_name] = 0

		for i in range(int((end - start) / increment)):
			temp_name = feature_name + "_" + str(i)
			if value > start + (increment * i) and value < start + (increment * (i + 1)):
				self.features[temp_name] = 1
			else:
				self.features[temp_name] = 0

	def extract_features_from_state(self, game_state):
		self.features = {}

		player = game_state.player
		platforms = game_state.platforms
		hammers = game_state.hammers
		distance_to_facing_platform = 0
		if platforms:
			right_platform = platforms[1]
			left_platform = platforms[0]
			distance_to_right_platform = right_platform.x - player.x
			distance_to_left_platform = player.x - left_platform.x + SC.platform_width
			if player.acceleration > 0:
				distance_to_facing_platform = distance_to_right_platform
			else:
				distance_to_facing_platform = distance_to_left_platform
			gap_location = right_platform.x - (SC.platform_gap_size / 2)
			distance_to_gap = player.x + (player.width / 2) - gap_location
			distance_to_closest_platform = min(distance_to_left_platform, distance_to_right_platform)


			distance_to_gap_times_acc = distance_to_gap * player.acceleration
			self.add_discrete_features(distance_to_gap_times_acc, "distance_to_gap_times_acc", -500, 500, 20)

			distance_to_gap_times_acc_times_vel = distance_to_gap * player.acceleration * player.velocity
			self.add_discrete_features(distance_to_gap_times_acc_times_vel, "distance_to_gap_times_acc_times_vel", -1500, 1500, 100)
			#self.add_discrete_features(features, distance_to_left_platform, "distance_to_left_platform", -250, 250, 10)
			#self.add_discrete_features(features, distance_to_facing_platform, "distance_to_facing_platform", -250, 250, 10)
		
		#self.add_discrete_features(features, game_state.player.velocity, "player_velocity", -5, 5, 1)
		
		distance_to_left_edge = player.x
		distance_to_right_edge = SC.screen_width - player.x - player.width
		distance_to_closest_edge = min(distance_to_left_edge, distance_to_right_edge)
		#self.add_discrete_features(features, distance_to_closest_edge, "distance_to_closest_edge", 0, 200, 10)

		if player.acceleration > 0:
			distance_to_facing_edge = distance_to_right_edge
		else:
			distance_to_facing_edge = distance_to_left_edge
		#self.add_discrete_features(features, distance_to_facing_edge, "distance_to_facing_edge", 0, 200, 10)
		return self.features

	def estimate_state_score(self, game_state, action):
		next_state = deepcopy(game_state)
		next_state.update_state(action)
		features = self.extract_features_from_state(next_state)
		score = 0
		for feature, value in features.iteritems():
			score += value * self.weights[feature]
		return score

	def get_action(self, game_state):
		actions = QLearningPlayer.actions
		if random.random() < self.exploration_prob:
			return random.choice(actions)
		else:
			valueTrue = self.estimate_state_score(game_state, True)
			valueFalse = self.estimate_state_score(game_state, False)
			return valueTrue > valueFalse

	def normalize_weights(self):
		if self.weights:
			max_feature_weight = abs(self.weights.most_common(1)[0][1])
			if max_feature_weight > 0:
				for feature,value in self.weights.most_common():
					self.weights[feature] /= max_feature_weight

	def incorporate_feedback(self, game_state, action, reward, next_game_state):
		verbose = False
		actions = QLearningPlayer.actions
		prediction =  self.estimate_state_score(game_state, action)
		target = reward + (self.discount * max(self.estimate_state_score(next_game_state, next_action) for next_action in actions))
		residual = prediction - target
		if next_game_state.game_over:
			if verbose:
				print "prediction: " + str(prediction)
				print "target: " + str(target)
				print "reward: " + str(reward)
				print "residual: " + str(residual)
		for feature, value in self.extract_features_from_state(game_state).iteritems():
			if verbose:
				print "weights before: " + str(self.weights)
				print "feture value: " + str(value)
			self.weights[feature] -= self.step_size * residual * value
			if verbose:
				print "weights after: " + str(self.weights)
		self.normalize_weights()