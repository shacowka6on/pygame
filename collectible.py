import pygame
from settings import *
from spritesheet import SpriteSheet

class Collectible:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.rect = pygame.Rect(x, y, 15, 15)

        self.sprites = self.load_sprites()
        self.animation_speed = 0.8
        self.animation_timer = 0
        self.current_frame = 0

    def load_sprites(self):
        raise NotImplementedError

    def on_collect(self):
        raise NotImplementedError

    def check_collision(self, player_rect):
        return self.rect.colliderect(player_rect)

    def animate(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.sprites)

    def draw(self, screen, offset_x=0, offset_y=0):
        self.animate(0.1)
        if self.sprites[self.current_frame]:
            current_image = self.sprites[self.current_frame]
        screen.blit(current_image, (self.pos.x - offset_x, self.pos.y - offset_y))

class Heart(Collectible):
    def load_sprites(self):
        images_dict = SpriteSheet.load_collectable_images("heart")
        return [images_dict[key] for key in sorted(images_dict.keys())]
    
    def on_collect(self, player):
        player.health = min(player.health + 20, 100)
    
    def collect_heart(self, player, hearts):
        for heart in hearts[:]:
            if heart.check_collision(player.rect) and player.health < 100:
                hearts.remove(heart)
                heart.on_collect(player)

class Overhealth(Collectible):
    def load_sprites(self):
        images_dict = SpriteSheet.load_collectable_images("overhealth")
        return [images_dict[key] for key in sorted(images_dict.keys())]
    
    def on_collect(self, player):
        player.health += 30

    def collect_overhealth(self, player, overhealths):
        for overhealth in overhealths[:]:
            if overhealth.check_collision(player.rect):
                overhealths.remove(overhealth)
                overhealth.on_collect(player)