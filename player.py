# -*- coding: utf-8 -*-
"""
Created on Sun Nov 01 18:04:22 2015

@author: Nolan
"""
import pygame
from pygame import transform
import math

class Player:
    height = 80
    width = 80
    image = transform.scale(pygame.image.load("orange_square.png"), (width, height)) 

    def __init__(self, starting_position, acceleration, velocity):
        self.x = starting_position[0]
        self.y = starting_position[1]
        self.acceleration = acceleration
        self.velocity = velocity
        
        self.image = Player.image
        self.player_rect = self.image.get_rect(center=starting_position)
    
    def update_position(self):
        self.velocity += self.acceleration
        # self.x += math.floor(self.velocity)
        
        speed = [self.velocity, 0]
        self.player_rect = self.player_rect.move(speed)
        self.x = self.player_rect.x
    
    def set_acceleration(self, acceleration):
        self.acceleration = acceleration
    
    def change_acceleration(self):
        self.acceleration = -self.acceleration
    
    def draw_player(self, surface):
        surface.blit(self.image, self.player_rect)
    
    def print_info(self):
        print "Position: " + str(self.x) + "," + str(self.y) + " Velocity: " + str(self.velocity) + " Acceleration: " + str(self.acceleration)
    
        
    