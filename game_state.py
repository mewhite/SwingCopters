# -*- coding: utf-8 -*-
"""
Created on Sat Nov 07 15:12:29 2015

@author: Nolan
"""
import swing_copter
from platform import Platform
from hammer import Hammer
import random
from swing_copter_constants import SC
from copy import deepcopy


class GameState:
    def __init__(self, player, platforms, hammers, frame_count, game_over=False, score=0):
        self.frame_count = frame_count
        self.player = player
        self.platforms = platforms
        self.hammers = hammers
        self.score = score
        self.game_over = game_over
        self.frozen_frames = 0

    def detect_collision(self):
        p_rect = self.player.player_rect
        if p_rect.left < 0 or p_rect.right > SC.screen_width:
            return True
        
        for platform in self.platforms:
            if p_rect.colliderect(platform.rect):
                return True
                
        for hammer in self.hammers:
            if p_rect.colliderect(hammer.collision_rect):
                return True
                
        return False
    
    def create_platforms(self):
        platform_x = random.randint(SC.platform_range[0], SC.platform_range[1])

        platform_position1 = (platform_x, SC.platform_start_y)
        platform_position2 = (platform_x + SC.platform_width + SC.platform_gap_size, SC.platform_start_y)
        
        hammer_x = random.randint(SC.platform_range[0], SC.platform_range[1])
        hammer_position1 = (platform_x + .9 * SC.platform_width - Hammer.default_width, SC.platform_start_y + SC.platform_height)

        hammer_position2 = (platform_x + SC.platform_width + SC.platform_gap_size + .1 * SC.platform_width, 
            SC.platform_start_y + SC.platform_height)

        first_platform = Platform(platform_position1, SC.platform_velocity)
        self.platforms.append(first_platform)
        second_platform = Platform(platform_position2, SC.platform_velocity)
        self.platforms.append(second_platform)
        """
        first_hammer = Hammer(hammer_position1, SC.platform_velocity)
        self.hammers.append(first_hammer)
        second_hammer = Hammer(hammer_position2, SC.platform_velocity)
        self.hammers.append(second_hammer)"""

    def update_positions(self):        
        self.player.update_position()
        
        for platform in self.platforms:
            platform.update_position()
    
        for hammer in self.hammers:
            hammer.update_position()

        if (self.platforms and self.platforms[0].y > self.player.y + SC.platform_height):
            self.platforms.popleft()
            self.platforms.popleft()
            if self.hammers:
                self.hammers.popleft()
                self.hammers.popleft()
            
            self.score += 1
            
        #if (self.platforms and self.platforms[0].y > self.player.y):
        
    def update_state(self, player_input, create_platforms=True):
        # Handle input
        if self.frozen_frames == 0 and player_input:
            if self.player.acceleration == 0:
                self.player.set_acceleration(SC.initial_player_accel)
            else:
                self.player.change_acceleration()
            self.frozen_frames += SC.frozen_frames_after_input + 1

        self.update_positions()

        if self.detect_collision():
            self.game_over = True
        if create_platforms:
            if self.frame_count % SC.platform_frequency == 0:
                self.create_platforms()
        if self.frozen_frames > 0:
            self.frozen_frames -= 1
        self.frame_count += 1

    def get_next_state(self, player_action, create_platforms=True):
       next_state = deepcopy(self)
       next_state.update_state(player_action, create_platforms)
       return next_state        
    
    def get_actions(self):
        if self.frozen_frames > 0:
            return [False]
        else:
            return [True, False]
        