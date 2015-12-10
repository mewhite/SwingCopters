# -*- coding: utf-8 -*-
"""
Created on Sun Nov 01 19:25:34 2015

@author: Nolan
"""
import pygame
from pygame import transform


class Hammer:
    default_height = 118
    default_width = 64
    default_image = transform.scale(pygame.image.load("rectangle.png"), (default_width, default_height))

    def __init__(self, starting_position, y_velocity):
        self.x = starting_position[0]
        self.y = starting_position[1]
        self.y_velocity = y_velocity
        self.x_direction = 1

        self.start_rotation = 0
        self.max_rotation = 45
        self.rotation_increment = 1

        self.height = Hammer.default_height
        self.width = Hammer.default_width
        self.image = Hammer.default_image
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.fill((249, 255, 255, 255))
        #self.rect = self.image.get_rect(topleft = starting_position)
        self.rotation = 0 #90 is vertical
        
        self.collision_rect = self.rect

    def update_position(self):
        self.y += self.y_velocity        
        speed = [0, self.y_velocity]
        self.rect = self.rect.move(speed)
        self.rotation += self.rotation_increment * self.x_direction
        if abs(self.rotation - self.start_rotation) > self.max_rotation:
            self.x_direction *= -1
        if self.rotation < self.start_rotation:
            if self.x_direction == -1:
                self.x -= 1.5
            if self.x_direction == 1:
                self.x += 1.5
        self.rect.topleft = ( self.x, self.y)
    
    def draw_hammer(self, surface):
        display_hammer = transform.rotate(self.image, self.rotation)
        self.collision_rect = display_hammer.get_rect(topleft=self.rect.topleft)
        surface.blit(display_hammer, self.rect)
