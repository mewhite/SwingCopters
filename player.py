# -*- coding: utf-8 -*-
"""
Created on Sun Nov 01 18:04:22 2015

@author: Nolan
"""
import pygame

class Player:
    default_image = pygame.image.load("square.png")
    def __init__(self, starting_position, acceleration, velocity, image=default_image):
        self.x = starting_position[0]
        self.y = starting_position[1]
        self.acceleration = acceleration
        self.velocity = velocity
        
        self.image = image
        self.player_rect = self.image.get_rect(center=starting_position)
    
    def update_position(self):
        self.velocity += self.acceleration
        self.x += self.velocity
        
        speed = [self.velocity, 0]
        self.player_rect = self.player_rect.move(speed)
    
    def set_acceleration(self, acceleration):
        self.acceleration = acceleration
    
    def change_acceleration(self):
        self.acceleration = -self.acceleration
    
    def draw_player(self, surface):
        surface.blit(self.image, self.player_rect)
    
    def print_info(self):
        print "Position: " + str(self.x) + "," + str(self.y) + " Velocity: " + str(self.velocity) + " Acceleration: " + str(self.acceleration)
    
        
    