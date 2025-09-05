import pygame

PLAYER_SPEED = 250
ANIMATION_COOLDOWN = 100
FRAME_WIDTH = 44
FRAME_HEIGHT = 44
SCALE = 2

BACKGROUND_COLOR = (50,50,50)

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock() 