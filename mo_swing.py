# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 16:31:20 2015

@author: Monisha
"""

import sys, pygame, time

from pygame import transform
from operator import add

def elementwise_add(list1, list2):
    return map(add, list1, list2)
    
pygame.init()

size = width, height = 800, 600
black = 255, 255, 255
screen = pygame.display.set_mode(size)

hammer = pygame.image.load("rectangle.png")
hammer = transform.scale(hammer, (70, 10))
start_pos = (width / 2 - 10, height / 5)

hammerrect = hammer.get_rect(center=start_pos)
hammerrect.center = start_pos 


screen.blit(hammer, hammerrect)
rotation = 90
direction = 1
xpos = width / 2 - 10
while 1:
    newhammer = transform.rotate(hammer, rotation)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    if direction == 1:
        rotation += 1
        if rotation > 135:
            direction = -1
    if direction == -1:
        rotation -= 1
        if rotation < 45:
            direction = 1
    if 45 < rotation < 90:
        if direction == -1:
            xpos -= 1
        if direction == 1:
            xpos += 1
    hammerrect.center = ( xpos, width / 5)


    screen.fill(black)

    screen.blit(newhammer, hammerrect)
    pygame.display.flip()
    time.sleep(0.01)