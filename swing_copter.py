# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 16:31:20 2015

@author: Nolan
"""

import sys, pygame, time
from player import Player
from wall import Wall
from hammer import Hammer
import random
from collections import deque


class SwingCopters:
    screen_size = screen_width, screen_height = 480, 600
    player_start_pos = (screen_width / 2, screen_height * 4/5)
    wall_velocity = 1
    initial_player_accel = 0.3
    background = 255, 255, 255
    frame_time = 0.01
    wall_gap_size = 200
    wall_frequency = 300
    wall_width = Wall.default_image.get_rect().width
    wall_height = Wall.default_image.get_rect().height
    wall_range = (int(-.9 * wall_width), int(screen_width - wall_gap_size - 1.1 * wall_width))
    #wall_range = (int(-.8 * wall_width), int(screen_width - .8 * wall_width - wall_gap_size))
    #wall_range = (0, 0 )

    print "Range: " + str(wall_range)
    
    def __init__(self):
        self.num_walls = 0
        self.num_hammers = 0

        pygame.init()
        self.frame_count = 0

        self.screen = pygame.display.set_mode(SwingCopters.screen_size)

        self.player = Player(SwingCopters.player_start_pos, 0, 0)
        self.walls = deque()
        self.hammers = deque()
        
    def create_walls(self):
        wall_x = random.randint(SwingCopters.wall_range[0], SwingCopters.wall_range[1])
        print wall_x
        wall_position1 = (wall_x, 0)
        wall_position2 = (wall_x + SwingCopters.wall_width + SwingCopters.wall_gap_size, 0)
        
        hammer_x = random.randint(SwingCopters.wall_range[0], SwingCopters.wall_range[1])
        hammer_position1 = (wall_x + .9 * SwingCopters.wall_width, SwingCopters.wall_height)

        hammer_position2 = (wall_x + SwingCopters.wall_width + SwingCopters.wall_gap_size + .1 * SwingCopters.wall_width, 
            SwingCopters.wall_height)


        

        first_wall = Wall(wall_position1, SwingCopters.wall_velocity)
        self.walls.append(first_wall)
        second_wall = Wall(wall_position2, SwingCopters.wall_velocity)
        self.walls.append(second_wall)
        
        self.num_walls += 2


        first_hammer = Hammer(hammer_position1, SwingCopters.wall_velocity)
        self.hammers.append(first_hammer)
        second_hammer = Hammer(hammer_position2, SwingCopters.wall_velocity)
        self.hammers.append(second_hammer)
        
        self.num_hammers += 2
    
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

    def detect_collision(self):
        return False
        p_rect = self.player.player_rect
        if p_rect.left < 0 or p_rect.right > SwingCopters.screen_width:
            return True
        
        for wall in self.walls:
            if p_rect.colliderect(wall.rect):
                return True
        return False

        
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.player.acceleration == 0:
                        self.player.set_acceleration(SwingCopters.initial_player_accel)
                    else:
                        self.player.change_acceleration()
                        
    def restart(self):
        self.player = Player(SwingCopters.player_start_pos, 0, 0)
        self.walls = deque()
        self.num_walls = 0
    
    def run_game(self):
        while 1:
            self.handle_input()
            if self.detect_collision():
                self.restart()
            self.update_display()
            self.frame_count += 1
            if self.frame_count % SwingCopters.wall_frequency == 0:
                self.create_walls()
            time.sleep(SwingCopters.frame_time)
            