import random
import swing_copter
from swing_copter_constants import SC
from collections import Counter
from copy import deepcopy
import math
import numpy
import pygame

#Q learning game player
class QLearningPlayer:
	actions = [True, False]
	def __init__(self, exploration_prob=0.0, step_size=.01, discount=.75):
		self.exploration_prob = exploration_prob
		self.weights = Counter()
		self.step_size = step_size
		self.discount = discount

	def add_discrete_features(self, features, value, feature_name, start, end, increment):
		temp_name = feature_name + "_-"
		if value < start:
			features[temp_name] = 1
		else:
			features[temp_name] = 0

		temp_name = feature_name + "_+"
		if value > end:
			features[temp_name] = 1
		else:
			features[temp_name] = 0

		for i in range(int((end - start) / increment)):
			temp_name = feature_name + "_" + str(start + (increment * i))
			if value > start + (increment * i) and value < start + (increment * (i + 1)):
				features[temp_name] = 1
			else:
				features[temp_name] = 0

	def extract_features_from_state(self, game_state, verbose=False):
		features = {}

		center = SC.screen_width / 2
		player = game_state.player
		platforms = game_state.platforms
		hammers = game_state.hammers
		x_distance_to_facing_platform = 0
		x_distance_to_left_edge = player.x
		x_distance_to_right_edge = SC.screen_width - player.x - player.width
		x_distance_to_closest_edge = min(x_distance_to_left_edge, x_distance_to_right_edge)
		abs_velocity = abs(player.velocity)
		if platforms:
			right_platform = platforms[1]
			left_platform = platforms[0]
			x_distance_to_right_platform = right_platform.x - player.x
			x_distance_to_left_platform = player.x - left_platform.x + SC.platform_width
			if player.acceleration > 0:
				x_distance_to_facing_platform = x_distance_to_right_platform
			else:
				x_distance_to_facing_platform = x_distance_to_left_platform
			gap_center = right_platform.x - (SC.platform_gap_size / 2.0)
			gap_left = gap_center - SC.platform_gap_size / 2.0
			gap_right = gap_center + SC.platform_gap_size / 2.0
			x_distance_to_gap = player.x + (player.width / 2.0) - gap_center
			x_distance_to_closest_platform = min(x_distance_to_left_platform, x_distance_to_right_platform)
			y_distance_to_platforms = player.y - (right_platform.y + right_platform.default_height)

			def get_stopping_dist_from_platform():
				x_i = game_state.player.x
				v_i = game_state.player.velocity
				if v_i > 0:
					platform_to_avoid = "right"
					x_i = x_i + game_state.player.width
					acc = -SC.initial_player_accel
				else:
					platform_to_avoid = "left"
					acc = SC.initial_player_accel
				x_f = -1 * v_i * v_i / (2 * acc) + x_i
				if platform_to_avoid == "right":
					return right_platform.x - x_f
				else:
					return x_f - (left_platform.x + SC.platform_width)
			stopping_dist_from_platform = get_stopping_dist_from_platform()
			if stopping_dist_from_platform < 4:# and y_distance_to_platforms > 0:
				features["too_late_to_stop_by_platform"] = 1
			if stopping_dist_from_platform < 10:# and y_distance_to_platforms > 0:
				features["<10_to_stop_by_platform"] = 1
			if stopping_dist_from_platform < 20:# and y_distance_to_platforms > 0:
				features["<20_to_stop_by_platform"] = 1
			if stopping_dist_from_platform < 50:# and y_distance_to_platforms > 0:
				features["<50_to_stop_by_platform"] = 1
			if stopping_dist_from_platform < 100:# and y_distance_to_platforms > 0:
				features["<100_to_stop_by_platform"] = 1

			#stopping_dist_from_hammer = get_stopping_dist_from_hammer"""

		def get_stopping_dist_from_wall():
			x_i = game_state.player.x
			v_i = game_state.player.velocity
			if v_i > 0:
				wall_to_avoid = "right_wall"
				x_i = x_i + game_state.player.width
				acc = -SC.initial_player_accel
			else:
				wall_to_avoid = "left_wall"
				acc = SC.initial_player_accel
			x_f = -1 * v_i * v_i / (2 * acc) + x_i
			if wall_to_avoid == "right_wall":
				return SC.screen_width - x_f
			else:
				return x_f


		stopping_dist_from_wall = get_stopping_dist_from_wall();

		if stopping_dist_from_wall < 4:
			features["too_late_to_stop_by_wall"] = 1
		if stopping_dist_from_wall < 10:
			features["<10_to_stop_by_wall"] = 1
		if stopping_dist_from_wall < 50:
			features["<50_to_stop_by_wall"] = 1
		if stopping_dist_from_wall < 100:
			features["<100_to_stop_by_wall"] = 1
		"""if stopping_dist_from_wall < 500:
			features["<500_to_stop_by_wall"] = 1"""

		if platforms:
			steps = 5
			def get_y_dist_needed_to_get_to_gap():
				x_i = game_state.player.x + .5 * game_state.player.acceleration * steps * steps + game_state.player.velocity * steps
				v_i = game_state.player.velocity + game_state.player.acceleration * steps
				v_y_i = SC.platform_velocity
				gap_center = game_state.platforms[1].x - SC.platform_gap_size / 2.0
				#if player is within gap space, no time or vertical distance is needed to get within the gap space
				if gap_center - SC.platform_gap_size / 2.0 < x_i and x_i + game_state.player.width < gap_right:
					return 0
				#if player is to the right of the gap, we want to ensure he can make it past the right platform
				x_i = x_i + game_state.player.width / 2
				if x_i > gap_center:
					x_i = x_i + game_state.player.width
					acc = -SC.initial_player_accel
					x_f = gap_center + SC.platform_gap_size / 2.0
				else:
					acc = SC.initial_player_accel
					x_f = gap_center - SC.platform_gap_size / 2.0
				x_f = gap_center

				time_needed = (-1 * v_i - math.sqrt(v_i * v_i - 2 * acc * (x_i - x_f))) / acc
				if time_needed < 0:
					time_needed = (-1 * v_i + math.sqrt(v_i * v_i - 2 * acc * (x_i - x_f))) / acc
				y_dist = v_y_i * time_needed
				return y_dist
			
			y_dist_needed_to_make_gap = get_y_dist_needed_to_get_to_gap()
			if y_distance_to_platforms - y_dist_needed_to_make_gap < 10 and y_distance_to_platforms > 0:
				features["not_enough_time_to_make_gap"] = 1


		return features

	def estimate_state_score(self, game_state, action, verbose=False):
		next_state = deepcopy(game_state)
		next_state.update_state(action)
		features = self.extract_features_from_state(next_state, verbose)
		
		score = 0
		for feature, value in features.iteritems():
			if verbose:
				print "feature: " + str(feature)
			score += value * self.weights[feature]

		return score

	def get_action(self, game_state,verbose=False):
		actions = game_state.get_actions()
		if len(actions) == 1:
			return actions[0]
		if random.random() < self.exploration_prob:
			return random.choice(actions)
		else:
			if verbose:
				print "###################"
				print "Change direction"
			valueTrue = self.estimate_state_score(game_state, True, verbose)
			if verbose:
				print "Don't change"
			valueFalse = self.estimate_state_score(game_state, False, verbose)
			if verbose:
				if valueTrue > valueFalse:
					print "Chose to change"
				else:
					print "-> Chose not to change"
			return valueTrue > valueFalse

	def normalize_weights(self):
		if self.weights:
			normalizer = 1
			for feature, value in self.weights.most_common():
				if abs(value) > normalizer:
					normalizer = value
			for feature,value in self.weights.most_common():
				self.weights[feature] /= normalizer
			"""max_feature_weight = abs(self.weights.most_common(1)[0][1])
			if max_feature_weight > 0:
				for feature,value in self.weights.most_common():
					self.weights[feature] /= max_feature_weight"""

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