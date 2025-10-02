import pygame

# Screen settings
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
BACKGROUND_COLOR = (50, 50, 50)

#Enviornment 
GRAVITY = 0.8
FLOOR = HEIGHT - 50

# Player settings
MOVE_SPEED = 250
JUMP_FORCE = 15

# Enemy settings
ENEMY_HEALTH = 100
ENEMY_SPEED = 150
ENEMY_ATTACK_RANGE = 80  
ENEMY_ATTACK_COOLDOWN = 500
ENEMY_DETECTION_RANGE = 300  
ENEMY_DAMAGE = 10
BULLET_DAMAGE = 35
PLAYER_DAMAGE = 25  # Damage enemy does to player

# Animation settings
FRAME_WIDTH = 44
FRAME_HEIGHT = 44
SCALE = 2
ANIMATION_COOLDOWN = 100  

# Combat settings
SHOOT_COOLDOWN = 200  
BULLET_SPEED = 10
BULLET_DAMAGE = 30