import pygame
import time
import sys
import numpy as np
pygame.init()


# variables
x = 1000
y = 1000
pos_x = x / 2
pos_y = y / 2
mass = 1 #kg ig
radius = 10 #cm
g = 9.81
dT = pygame.time.Clock().tick(60) / 1000  # convert milliseconds to seconds
# 1 pixel = 1 m
vel_y = 0
vel_x = 0
gravity = True
onground = False
acceleration = 1
maxX = 20
def jump():
    global vel_y, gravity, onground
    if onground:
        vel_y = -10
        onground = False
def moveX(direction):
    global pos_x, vel_x
    if vel_x < maxX and vel_x > -maxX:
        vel_x += acceleration * direction
        print(f"Horizontal velocity is {vel_x}")
    else:
        vel_x = maxX * direction
        print(f"Horizontal velocity is {vel_x}")
    pos_x += vel_x
    time.sleep(dT)

#region INITIALZATION STUFFS
screen = pygame.display.set_mode((x, y))
pygame.display.set_caption("gam")
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jump()
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_a, pygame.K_d):
                vel_x = 0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        moveX(-1)
    if keys[pygame.K_d]:
        moveX(1)
        if event.type == pygame.QUIT:
            running = False
#endregion

    if not onground: #GRAVITY BABY
        if vel_y < np.sqrt((2 * mass * g) / (1.225 * np.pi * (radius / 100)**2 * 0.47)): #terminal velocity ~ 32.93499424250039
                vel_y += (g * dT)
                print(f"velocity is {vel_y}")
                pos_y +=vel_y 
        time.sleep(dT)
    
    if pos_y >= y - radius:
        pos_y = y - radius
        onground = True
    
    if pos_x >= x - radius:
        pos_x = x - radius
    if pos_x <= radius:
        pos_x = radius

    
    
            
        #region end of  initialization stuffs
    screen.fill((255, 255, 255))  # white
    pygame.draw.circle(screen, (0, 0, 0), [pos_x, pos_y], radius, 0) #black circle
    pygame.display.flip()
#endregion
pygame.quit()