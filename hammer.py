# -*- coding: utf-8 -*-
"""
Created on Sun Nov 01 19:25:34 2015

@author: Nolan
"""
import pygame
from pygame import transform


class Hammer:
    default_image = pygame.image.load("rectangle.png")
    default_height = 100
    default_width = 15
    def __init__(self, starting_position, y_velocity, image=default_image, height=default_height, width=default_width):
        self.x = starting_position[0]
        self.y = starting_position[1]
        self.y_velocity = y_velocity
        self.x_direction = 1

        self.start_rotation = 90
        self.max_rotation = 45
        self.rotation_increment = 1

        self.height = height
        self.width = width
        self.image = transform.scale(image, (self.height, self.width))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(topleft = starting_position)
        self.rotation = 90 #90 is vertical
        
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
