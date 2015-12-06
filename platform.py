# -*- coding: utf-8 -*-
"""
Created on Sun Nov 01 19:25:34 2015

@author: Nolan
"""
import pygame
from pygame import transform


class Platform:
    default_height = 38
    default_width = 354
    default_image = transform.scale(pygame.image.load("platform.png"), (default_width, default_height))

    def __init__(self, starting_position, velocity):
        self.x = starting_position[0]
        self.y = starting_position[1]
        self.velocity = velocity
        
        self.image = Platform.default_image
        
        self.rect = self.image.get_rect(topleft = starting_position)
        
    def update_position(self):
        self.y += self.velocity        
        speed = [0, self.velocity]
        self.rect = self.rect.move(speed)
    
    def draw_platform(self, surface):
        surface.blit(self.image, self.rect)