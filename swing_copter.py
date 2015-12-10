# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 16:31:20 2015

@author: Nolan
"""

import sys, pygame, time
from player import Player
from platform import Platform
from hammer import Hammer
from collections import deque
import game_state
from copy import deepcopy
from swing_copter_constants import SC
from qlearn_player import QLearningPlayer
import mcts
import math

class SwingCopters:

    def __init__(self, display_game=True):
        pygame.init()
        #self.font = pygame.font.Font(None, 60)
        self.playing = False
        self.display_game = display_game
        if self.display_game:
            self.screen = pygame.display.set_mode(SC.screen_size)

        player = Player(SC.player_start_pos, SC.initial_player_accel, 0)
        platforms = deque()
        hammers = deque()
        
        self.game_state = game_state.GameState(player, platforms, hammers, 0, False)
        
    def detect_input(self):
        is_input = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    is_input = True
        return is_input
                        
    def restart(self):
        player = Player(SC.player_start_pos, SC.initial_player_accel, 0)
        platforms = deque()
        hammers = deque()
        self.game_state = game_state.GameState(player, platforms, hammers, 0, False)
        self.playing = False
    
    def draw_state(self):
        self.screen.fill(SC.background)
        self.game_state.player.draw_player(self.screen)
        
        for platform in self.game_state.platforms:
            platform.draw_platform(self.screen)
    
        for hammer in self.game_state.hammers:
            hammer.draw_hammer(self.screen)
        
        #score_display = self.font.render(str(self.game_state.score), 0, SC.score_color, SC.background)
        #self.screen.blit(score_display, (10, 10))
        pygame.display.flip()
        
    def run_human_player(self, num_games = -1):
        scores = []
        while 1:
            is_input = self.detect_input()
            if is_input:
                self.playing = True
            if self.playing:
                self.game_state.update_state(is_input)
                if self.game_state.game_over:
                    scores.append(self.game_state.frame_count)
                    num_games -= 1
                    if num_games == 0:
                        print self.game_state.frame_count
                        return scores
                    self.restart()
            self.draw_state()
            time.sleep(SC.frame_time)

    def run_qlearning_player(self, num_games=1):
        self.game_state.update_state(True)
        game_player = QLearningPlayer()
        self.game_state.player.acceleration = 1
        scores = []
        n = 0
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
            action = game_player.get_action(self.game_state)
            prev_game_state = deepcopy(self.game_state)
            self.game_state.update_state(action)
            reward = 0
            if self.game_state.game_over:
                print game_player.weights
                print "game over"
                reward = -10
                game_player.incorporate_feedback(prev_game_state, action, reward, self.game_state)
                print game_player.weights
                scores.append(self.game_state.frame_count)
                n += 1
                if n == num_games:
                    return scores
                self.restart()
            else:
                game_player.incorporate_feedback(prev_game_state, action, reward, self.game_state)
            self.draw_state()

    def simulate_game_from_state(self,game_state):
        self.game_state = game_state
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
            action = False
            prev_game_state = deepcopy(self.game_state)
            self.game_state.update_state(action)
            if self.game_state.game_over:
                return self.game_state.get_collider()
            self.draw_state()

    def run_mcts_player(self, num_games=10):
        full_mobility = True
        scores = []
        self.game_state.update_state(True)
        game_number = 0
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return scores
            if not full_mobility:
                if self.game_state.frame_count % 10 == 0:
                    action = mcts.get_MCTS_action(self.game_state)
                else:
                    action = False
            else:
                action = mcts.get_MCTS_action(self.game_state)
            #print "Action: " + str(action)
            prev_game_state = deepcopy(self.game_state)
            self.game_state.update_state(action)
            if self.game_state.game_over:
                scores.append(self.game_state.frame_count)
                print "Game number: " + str(game_number)
                print "Frame Count: " + str(self.game_state.frame_count)
                game_number += 1
                if game_number == num_games: 
                    return scores
                self.restart()
            if self.display_game:
                self.draw_state()
