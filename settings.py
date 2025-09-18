import pygame

# Screen settings
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
BACKGROUND_COLOR = (50, 50, 50)

#Enviornment 
GRAVITY = 0.8
FLOOR = HEIGHT * 0.9 

# Player settings
MOVE_SPEED = 250
JUMP_FORCE = 15

# Animation settings
FRAME_WIDTH = 44
FRAME_HEIGHT = 44
SCALE = 2
ANIMATION_COOLDOWN = 100  

# Combat settings
SHOOT_COOLDOWN = 200  
BULLET_SPEED = 10