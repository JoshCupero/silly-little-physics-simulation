import pygame
import sys
import math
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
acceleration = 500
maxXVel = 800 #max horizontal velocity
jumpVel = 800 #jump velocity
tvel = math.sqrt((2 * m * 981) / (1.225 * math.pi * (radiusP/100)**2 * 0.47)) #terminal velocity
μ = 2 #friction coefficient
CoR = 0.8 #coefficient of restitution

#preferences
bounce = 0

#game
screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("gam")
game_state = "start_menu"
def draw_start_menu():
    screen.fill((255, 255, 255))  # white
    font = pygame.font.Font(None, 74)
    text = font.render("Press SPACE to Start", True, (0, 0, 0))
    bounce_button = font.render("Press B to Toggle Bounce", True, (0, 0, 0))
    text_rect = text.get_rect(center=(Width / 2, Height / 2))
    bounce_button_rect = bounce_button.get_rect(center=(Width / 2, Height / 2 + 100))
    screen.blit(text, text_rect)
    screen.blit(bounce_button, bounce_button_rect)
    pygame.display.flip()

draw_start_menu()

def jump():
    global vel_y, on_ground
    if bounce == 0:
        if on_ground:
            vel_y = -jumpVel 
            on_ground = False
    if bounce == 1:
        if y > 920:
            vel_y = -jumpVel
            on_ground = False

def moveX(direction):
    global x, vel_x
    if (vel_x < maxXVel and vel_x > -maxXVel) and on_ground:
        vel_x += (acceleration * dt) * direction
        print(f"Horizontal velocity is {vel_x}")
    elif (vel_x >= maxXVel or vel_x <= -maxXVel) and on_ground:
        vel_x = maxXVel * direction
        print(f"Horizontal velocity is {vel_x}")
    elif (vel_x < maxXVel and vel_x > -maxXVel) and bounce == 1:
        vel_x += (acceleration * dt) * direction
        print(f"Horizontal velocity is {vel_x}")




running = True
while running:
    dt = clock.tick(FPS) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if game_state == "start_menu":
                if event.key == pygame.K_SPACE:
                    game_state = "game"
                if event.key == pygame.K_b:
                    bounce = 0 if bounce == 1 else 1
            elif game_state == "game":
                if event.key == pygame.K_SPACE:
                    jump()
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_a, pygame.K_d):
                not_moving = True

    if game_state == "start_menu":
        draw_start_menu()
        continue

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        not_moving = False
        moveX(-1)
    if keys[pygame.K_d]:
        not_moving = False
        moveX(1)

    #gravity
    if not on_ground: 
        if vel_y < tvel:
                vel_y += (g * dt)
                print(f"velocity is {vel_y}")
        else:
            vel_y = tvel
            print(f"velocity is {vel_y}")
            
    #friction
    if not_moving and on_ground:
        if vel_x > 10:
            vel_x -= μ * g * dt
            print(f"Horizontal velocity is {vel_x}")
        if vel_x < -10:
            vel_x += μ * g * dt
            print(f"Horizontal velocity is {vel_x}")
    
    #move
    x += vel_x * dt
    y += vel_y * dt

    #on ground
    if y >= Height - radiusP:
        y = Height - radiusP
        if bounce == 1:
            vel_y = -vel_y * bounce * CoR
        else:
            on_ground = True
            vel_y = 0
    #hit wall
    if x >= Width - radiusP:
        x = Width - radiusP
        vel_x = -vel_x * bounce * CoR
    if x <= radiusP:
        x = radiusP
        vel_x = vel_x * -1 * bounce * CoR
    #draw
    screen.fill((255, 255, 255))  # white
    pygame.draw.circle(screen, (0, 0, 0), [x, y], radiusP, 0) #black circle
    pygame.display.flip()

pygame.quit()
sys.exit()