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
			gap_location = right_platform.x - (SC.platform_gap_size / 2)
			x_distance_to_gap = player.x + (player.width / 2) - gap_location
			x_distance_to_closest_platform = min(x_distance_to_left_platform, x_distance_to_right_platform)
			y_distance_to_platforms = right_platform.y - player.y


			x_dist_sign = 1
			if x_distance_to_gap < 0 : x_dist_sign = -1
			signed_distance_to_gap =  x_dist_sign * math.sqrt(x_distance_to_gap*x_distance_to_gap + y_distance_to_platforms*y_distance_to_platforms)
			signed_distance_to_gap_times_acc = signed_distance_to_gap * player.acceleration
			#self.add_discrete_features(features, signed_distance_to_gap_times_acc, "signed_distance_to_gap_times_acc", -center, center, 20)


			x_distance_to_gap_times_acc = x_distance_to_gap * player.acceleration
			#self.add_discrete_features(features, x_distance_to_gap_times_acc, "x_distance_to_gap_times_acc", -500, 500, 20)
			use_discretized_distance_to_gap_times_acc = False
			if use_discretized_distance_to_gap_times_acc:
				if (y_distance_to_platforms < 20):
					self.add_discrete_features(features, x_distance_to_gap_times_acc, "y<20_x_distance_to_gap_times_acc", -500, 500, 50)
				if (20 <= y_distance_to_platforms < 50):
					self.add_discrete_features(features, x_distance_to_gap_times_acc, "y<50_x_distance_to_gap_times_acc", -500, 500, 50)
				if (50 <= y_distance_to_platforms < 100):
					self.add_discrete_features(features, x_distance_to_gap_times_acc, "y<100_x_distance_to_gap_times_acc", -500, 500, 50)
				if (100 <= y_distance_to_platforms < 200):
					self.add_discrete_features(features, x_distance_to_gap_times_acc, "y<200_x_distance_to_gap_times_acc", -500, 500, 50)
				if (200 <= y_distance_to_platforms < 500):
					self.add_discrete_features(features, x_distance_to_gap_times_acc, "y<500_x_distance_to_gap_times_acc", -500, 500, 50)
				if (500 <= y_distance_to_platforms):
					self.add_discrete_features(features, x_distance_to_gap_times_acc, "y>500_x_distance_to_gap_times_acc", -500, 500, 50)


		if not player.velocity == 0:
			dist_to_edge = player.x - SC.screen_width  #(signed_distance from right wall)
			if player.x < x_distance_to_right_edge:
				dist_to_edge = player.x
			dist_to_edge_over_vel_times_acc = dist_to_edge / player.velocity
			#self.add_discrete_features(features, dist_to_edge_over_vel_times_acc, "dist_to_edge_over_vel_times_acc", -400, 400, 50)
			use_discretized_dist_to_edge_over_vel_times_acc = False
			if use_discretized_dist_to_edge_over_vel_times_acc:
				if (-50 <= dist_to_edge < 0):
					self.add_discrete_features(features, dist_to_edge_over_vel_times_acc, "<-50_dist_to_edge_over_vel_times_acc", -500, 500, 50)
				if (0 <= dist_to_edge < 50):
					self.add_discrete_features(features, dist_to_edge_over_vel_times_acc, "50_dist_to_edge_over_vel_times_acc", -500, 500, 50)
				if (-100 <= dist_to_edge < -50):
					self.add_discrete_features(features, dist_to_edge_over_vel_times_acc, "<-100_dist_to_edge_over_vel_times_acc", -500, 500, 50)
				if (50 <= dist_to_edge < 100):
					self.add_discrete_features(features, dist_to_edge_over_vel_times_acc, "100_dist_to_edge_over_vel_times_acc", -500, 500, 50)
				

			x_distance_to_gap_times_vel_times_acc = x_distance_to_gap * player.acceleration
			#self.add_discrete_features(features, x_distance_to_gap_times_acc, "x_distance_to_gap_times_acc", -500, 500, 20)
			
			#self.add_discrete_features(features, signed_distance_to_gap, "signed_distance_to_gap", -center, center, 20)

			x_distance_to_gap_times_acc_times_vel = x_distance_to_gap * player.acceleration * player.velocity
			#self.add_discrete_features(features, x_distance_to_gap_times_acc_times_vel, "x_distance_to_gap_times_acc_times_vel", -1500, 1500, 100)
			#self.add_discrete_features(features, x_distance_to_left_platform, "x_distance_to_left_platform", -250, 250, 10)
			#self.add_discrete_features(features, x_distance_to_facing_platform, "x_distance_to_facing_platform", -250, 250, 10)

		#self.add_discrete_features(features, abs_velocity, "abs_velocity", 0, 5, .5)

		vel_times_accel = player.velocity * player.acceleration
		#self.add_discrete_features(features, vel_times_accel, "vel_times_accel", -5, 5, .5)

		#self.add_discrete_features(features, x_distance_to_closest_edge, "x_distance_to_closest_edge", 0, 200, 10)

		dist_from_center = center - player.x
		dist_from_center_times_vel_times_acc = dist_from_center * player.velocity * player.acceleration
		#self.add_discrete_features(features, dist_from_center_times_vel_times_acc, "dist_from_center_times_vel_times_acc", -center * 5, center * 5, 100)


		if player.acceleration > 0:
			x_distance_to_facing_edge = x_distance_to_right_edge
		else:
			x_distance_to_facing_edge = x_distance_to_left_edge
		#self.add_discrete_features(features, x_distance_to_facing_edge, "x_distance_to_facing_edge", 0, 200, 10)


		def simulate_game_from_state(start_game_state):
			game_state = start_game_state
			while 1:
				for event in pygame.event.get():
					if event.type == pygame.QUIT: sys.exit()
				action = False
				prev_game_state = deepcopy(game_state)
				game_state.update_state(action)
				if game_state.game_over:
					return game_state.get_collider()

		def too_late_to_stop_by_wall():
			#set acceleration to opposition direction and velocity and see if player will avoid hitting wall it's moving towards
			temp_game_state = deepcopy(game_state)
			temp_game_state.platforms = []
			temp_game_state.hammers = []
			if temp_game_state.player.velocity > 0:
				wall_to_avoid = "right_wall"
				temp_game_state.player.x += 5
				temp_game_state.player.acceleration = -1
			else:
				wall_to_avoid = "left_wall"
				temp_game_state.player.x -= 5
				temp_game_state.player.acceleration = 1
			display_game = True
			collider = simulate_game_from_state(temp_game_state)
			if collider == wall_to_avoid:
				return True
			return False

		"""if too_late_to_stop_by_wall():
			features["too_late_to_stop_by_wall"] = 1
		else:
			features["too_late_to_stop_by_wall"] = 0"""

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


		def get_y_dist_needed_to_get_to_gap():
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



		return features

	def estimate_state_score(self, game_state, action, verbose=False):
		next_state = deepcopy(game_state)
		next_state.update_state(action)
		features = self.extract_features_from_state(next_state, verbose)
		
		score = 0
		for feature, value in features.iteritems():
			score += value * self.weights[feature]

		return score

	def get_action(self, game_state):
		actions = QLearningPlayer.actions
		if random.random() < self.exploration_prob:
			return random.choice(actions)
		else:
			valueTrue = self.estimate_state_score(game_state, True, verbose=True)
			valueFalse = self.estimate_state_score(game_state, False, verbose=True)
			#if valueTrue != valueFalse:
			#	print "Diff!!!"
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