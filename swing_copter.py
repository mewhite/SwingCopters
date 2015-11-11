# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 16:31:20 2015

@author: Nolan
"""

import sys, pygame, time
from player import Player
from wall import Wall
from hammer import Hammer
from collections import deque
import game_state
from copy import copy


class SwingCopters:
    screen_size = screen_width, screen_height = 671, 744
    player_start_pos = (screen_width / 2, screen_height * 4/5)
    wall_velocity = 1
    initial_player_accel = 0.3
    background = 255, 255, 255
    score_color = 0, 0, 0
    frame_time = 0.007
    wall_gap_size = 317
    wall_frequency = 377
    wall_width = Wall.default_width
    wall_height = Wall.default_height
    wall_range = (int(-.9 * wall_width), int(screen_width - wall_gap_size - 1.1 * wall_width))
    wall_start_y = -200
    
    def __init__(self):
        pygame.init()
        self.font = pygame.font.Font(None, 60)
        self.frame_count = 0
        self.playing = False
        self.screen = pygame.display.set_mode(SwingCopters.screen_size)

        player = Player(SwingCopters.player_start_pos, 0, 0)
        walls = deque()
        hammers = deque()
        self.game_state = game_state.GameState(player, walls, hammers, 0, False)
    
    def update_display(self):
        self.screen.fill(SwingCopters.background)
        self.player.update_position()
        self.player.draw_player(self.screen)
        
        for wall in self.walls:
            wall.update_position()
            wall.draw_wall(self.screen)
    
        for hammer in self.hammers:
            hammer.update_position()
            hammer.draw_hammer(self.screen)

        if (self.num_walls > 0 and self.walls[0].y > SwingCopters.screen_height):
            self.walls.popleft()
            self.walls.popleft()
            self.num_walls -= 2

            self.hammers.popleft()
            self.hammers.popleft()
            self.num_hammers -= 2
            
        pygame.display.flip()
        
    def detect_input(self):
        is_input = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    is_input = True
        return is_input
                        
    def restart(self):
        player = Player(SwingCopters.player_start_pos, 0, 0)
        walls = deque()
        hammers = deque()
        self.game_state = game_state.GameState(player, walls, hammers, 0, False)
        self.playing = False
    
    def draw_state(self):
        self.screen.fill(SwingCopters.background)
        self.game_state.player.draw_player(self.screen)
        
        for wall in self.game_state.walls:
            wall.draw_wall(self.screen)
    
        for hammer in self.game_state.hammers:
            hammer.draw_hammer(self.screen)
        
        #score_display = self.font.render(str(self.game_state.score), 0, SwingCopters.score_color, SwingCopters.background)
        #self.screen.blit(score_display, (10, 10))
        pygame.display.flip()
        
    def run_game(self):
        while 1:
            is_input = self.detect_input()
            if is_input:
                self.playing = True
            if self.playing:
                self.game_state.update_state(is_input)
                if self.game_state.game_over:
                    self.restart()
            self.draw_state()
            time.sleep(SwingCopters.frame_time)
            