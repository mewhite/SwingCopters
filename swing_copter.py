# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 16:31:20 2015

@author: Nolan
"""

import sys, pygame, time

from operator import add

def elementwise_add(list1, list2):
    return map(add, list1, list2)
    
pygame.init()

size = width, height = 400, 600
start_pos = (width / 2, height * 4/5)
speed = [0, 0]
accel = 0
space_accel = 0.1
black = 255, 255, 255
screen = pygame.display.set_mode(size)
ball = pygame.image.load("square.png")
start_rect = ball.get_rect(center=start_pos)
ballrect = ball.get_rect(center=start_pos)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if accel == 0:
                    accel = -space_accel
                else:
                    accel = -accel
    speed[0] += accel 
    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        ballrect = start_rect
        speed = [0, 0]
        accel = 0
    if ballrect.top < 0 or ballrect.bottom > height:
        ballrect = start_rect
        speed = [0, 0]
        accel = 0
    screen.fill(black)
    screen.blit(ball, ballrect)
    pygame.display.flip()
    time.sleep(0.01)