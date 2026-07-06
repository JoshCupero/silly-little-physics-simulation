import pygame
import time
import sys
import numpy as np
pygame.init()


#======================variables===========================

#window
Width = 1000 #pixels
Height = 1000

#time/fps
clock = pygame.time.Clock()
FPS = 120

#circle
x = Width / 2 # pixels
y = Height / 2 # pixels
radiusP = 10 #radius in pixels

#physics
pixels_per_meter = 100 #pixels per meter
m = 1 #kg
g = 981 #pixels per second squared
vel_y = 0
vel_x = 0
on_ground = False
not_moving = True
acceleration = 1000
maxXVel = 1500 #max horizontal velocity
jumpVel = 800 #jump velocity
tvel = np.sqrt((2 * m * g) / (1.225 * np.pi * (radiusP/100)**2 * 0.47)) #terminal velocity
μ = 2 #friction coefficient



def jump():
    global vel_y, on_ground

    if on_ground:
        vel_y = -jumpVel 
        on_ground = False

def moveX(direction):
    global x, vel_x
    if vel_x < maxXVel and vel_x > -maxXVel:
        vel_x += (acceleration * dt) * direction
        print(f"Horizontal velocity is {vel_x}")
    else:
        vel_x = maxXVel * direction
        print(f"Horizontal velocity is {vel_x}")

#setup screen
screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("gam")


running = True
while running:
    dt = clock.tick(FPS) / 1000
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jump()
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_a, pygame.K_d):
                not_moving = True
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        not_moving = False
        moveX(-1)
    if keys[pygame.K_d]:
        not_moving = False
        moveX(1)

    if not on_ground: #gravity
        if vel_y < tvel:
                vel_y += (g * dt)
                print(f"velocity is {vel_y}")
        else:
            vel_y = tvel
            print(f"velocity is {vel_y}")
    #friction
    if not_moving and on_ground:
        if vel_x > 10:
            vel_x -= μ * m * g * dt
            print(f"Horizontal velocity is {vel_x}")
        if vel_x < -10:
            vel_x += μ * m * g * dt
            print(f"Horizontal velocity is {vel_x}")
    
    x += vel_x * dt
    y += vel_y * dt

    if y >= Height - radiusP:
        y = Height - radiusP
        on_ground = True
        vel_y = 0
    
    if x >= Width - radiusP:
        x = Width - radiusP
    if x <= radiusP:
        x = radiusP

    screen.fill((255, 255, 255))  # white
    pygame.draw.circle(screen, (0, 0, 0), [x, y], radiusP, 0) #black circle
    pygame.display.flip()

pygame.quit()
sys.exit()