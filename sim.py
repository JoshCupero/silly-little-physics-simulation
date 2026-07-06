import pygame
import time
import sys
import numpy as np
pygame.init()


#======================variables===========================

#window
Width = 1000
Height = 1000

#time/fps
clock = pygame.time.Clock()
FPS = 60

#circle
x = Width / 2
y = Height / 2
radiusM = 0.1 #meter
radiusP = 10 #radius in pixels

#physics
m = 1 #kg
g = 9.81
vel_y = 0
vel_x = 0
on_ground = False
acceleration = 2
maxXVel = 100 #max horizontal velocity
jumpVel = 100 #jump velocity
tvel = np.sqrt((2 * m * g) / (1.225 * np.pi * (radiusM)**2 * 0.47)) #terminal velocity

def jump():
    global vel_y, on_ground

    if on_ground:
        vel_y = -jumpVel 
        on_ground = False

def moveX(direction):
    global x, vel_x
    if vel_x < maxXVel and vel_x > -maxXVel:
        vel_x += acceleration * direction
        print(f"Horizontal velocity is {vel_x}")
    else:
        vel_x = maxXVel * direction
        print(f"Horizontal velocity is {vel_x}")
    x += vel_x * dt

#setup screen
screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("gam")


running = True
while running:
    dt = clock.tick(FPS) / 50
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

    if not on_ground: #gravity
        if vel_y < tvel:
                vel_y += (g * dt)
                print(f"velocity is {vel_y}")
        else:
            vel_y = tvel
            print(f"velocity is {vel_y}")
        y += vel_y * dt
        
    if y >= Height - radiusP:
        y = Height - radiusP
        on_ground = True
    
    if x >= Width - radiusP:
        x = Width - radiusP
    if x <= radiusP:
        x = radiusP

    screen.fill((255, 255, 255))  # white
    pygame.draw.circle(screen, (0, 0, 0), [x, y], radiusP, 0) #black circle
    pygame.display.flip()

pygame.quit()
sys.exit()