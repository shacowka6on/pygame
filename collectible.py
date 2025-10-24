import pygame
from settings import *
from spritesheet import SpriteSheet

class Collectible:
    def __init__(self,x,y,type):
        self.pos = pygame.Vector2(x,y)
        self.rect = pygame.Rect(x,y,15,15)
        self.type = type
        self.sprites = self.fill_sprites_dict()
        self.animation_speed = 0.1
        self.animation_timer = 0
        self.current_frame = 0

    def fill_sprites_dict(self):
        imgs = SpriteSheet.load_collectable_images(self.type)

        self.sprites = imgs
        return self.sprites
    
    def animate(self, dt):
        self.animation_timer += dt
        if self.animation_speed <= self.animation_timer:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.sprites)

    def draw(self):
        # img = next(iter(self.sprites.values()))
        # print(img)
        # screen.blit(img, (self.pos.x,self.pos.y))
        img = pygame.image.load(f"pygame/assets/collectibles/heart/heart1.png").convert()
        return img
        # screen.blit(img, (100,100))