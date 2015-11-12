# -*- coding: utf-8 -*-
"""
Created on Sat Nov 07 15:12:29 2015

@author: Nolan
"""
import swing_copter
from wall import Wall
from hammer import Hammer
import random
from swing_copter_constants import SC


class GameState:
    def __init__(self, player, walls, hammers, frame_count, game_over=False, score=0):
        self.frame_count = frame_count
        self.player = player
        self.walls = walls
        self.hammers = hammers
        self.score = score
        self.game_over = game_over

    def detect_collision(self):
        p_rect = self.player.player_rect
        if p_rect.left < 0 or p_rect.right > SC.screen_width:
            return True
        
        for wall in self.walls:
            if p_rect.colliderect(wall.rect):
                return True
                
        for hammer in self.hammers:
            if p_rect.colliderect(hammer.collision_rect):
                return True
                
        return False
    
    def create_walls(self):
        wall_x = random.randint(SC.wall_range[0], SC.wall_range[1])

        wall_position1 = (wall_x, SC.wall_start_y)
        wall_position2 = (wall_x + SC.wall_width + SC.wall_gap_size, SC.wall_start_y)
        
        hammer_x = random.randint(SC.wall_range[0], SC.wall_range[1])
        hammer_position1 = (wall_x + .9 * SC.wall_width - Hammer.default_width, SC.wall_start_y + SC.wall_height)

        hammer_position2 = (wall_x + SC.wall_width + SC.wall_gap_size + .1 * SC.wall_width, 
            SC.wall_start_y + SC.wall_height)

        first_wall = Wall(wall_position1, SC.wall_velocity)
        self.walls.append(first_wall)
        second_wall = Wall(wall_position2, SC.wall_velocity)
        self.walls.append(second_wall)

        first_hammer = Hammer(hammer_position1, SC.wall_velocity)
        self.hammers.append(first_hammer)
        second_hammer = Hammer(hammer_position2, SC.wall_velocity)
        self.hammers.append(second_hammer)

    def update_positions(self):        
        self.player.update_position()
        
        for wall in self.walls:
            wall.update_position()
    
        for hammer in self.hammers:
            hammer.update_position()

        if (self.walls and self.walls[0].y > SC.screen_height):
            self.walls.popleft()
            self.walls.popleft()

            self.hammers.popleft()
            self.hammers.popleft()
            
            self.score += 1
            
        #if (self.walls and self.walls[0].y > self.player.y):

    def update_state(self, player_input, create_walls=True):
        # Handle input
        if player_input:
            if self.player.acceleration == 0:
                self.player.set_acceleration(SC.initial_player_accel)
            else:
                self.player.change_acceleration()

        self.update_positions()

        if self.detect_collision():
            self.game_over = True
        if create_walls:
            if self.frame_count % SC.wall_frequency == 0:
                self.create_walls()

        self.frame_count += 1
        
        
        