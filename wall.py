# -*- coding: utf-8 -*-
"""
Created on Sun Nov 01 19:25:34 2015

@author: Nolan
"""
import pygame

class Wall:
    default_image = pygame.image.load("platform.png")
    def __init__(self, starting_position, velocity, image=default_image):
        self.x = starting_position[0]
        self.y = starting_position[1]
        self.velocity = velocity
        
        self.image = image
        
        self.rect = self.image.get_rect(center = starting_position)
        
    def update_position(self):
        self.y += self.velocity        
        speed = [0, self.velocity]
        self.rect = self.rect.move(speed)
    
    def draw_wall(self, surface):
        surface.blit(self.image, self.rect)