import pygame

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
BACKGROUND_IMG = pygame.image.load("pygame/assets/game_background/Background.png").convert()
BACKGROUND_IMG = pygame.transform.scale(BACKGROUND_IMG, (WIDTH, HEIGHT))
BACKGROUND_COLOR = (50, 50, 50)

#Enviornment 
GRAVITY = 0.4
FLOOR = HEIGHT - 50

# Player settings
MOVE_SPEED = 250
JUMP_FORCE = 15

# Enemy settings
ENEMY_HEALTH = 100
ENEMY_SPEED = 50
ENEMY_ATTACK_RANGE = 80  
ENEMY_ATTACK_COOLDOWN = 800
ENEMY_DETECTION_RANGE = 150  
ENEMY_DAMAGE = 15
BULLET_DAMAGE = 35

# Animation settings
FRAME_WIDTH = 44
FRAME_HEIGHT = 44
SCALE = 2
ANIMATION_COOLDOWN = 100  

# Bullet settings
SHOOT_COOLDOWN = 200  
BULLET_SPEED = 7
BULLET_DAMAGE = 30