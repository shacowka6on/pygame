import pygame
from settings import *

class Bullet:
    def __init__(self, x, y, target_x, target_y):
        self.pos = pygame.Vector2(x, y)
        direction = pygame.Vector2(target_x - x, target_y - y).normalize()
        self.velocity = direction * BULLET_SPEED

        self.original_image = pygame.image.load('pygame/assets/laserBullet.png').convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (20, 30))
        
        direction_vector = pygame.math.Vector2(target_x - x, target_y - y)
        angle = direction_vector.angle_to(pygame.math.Vector2(0, -1))
        print(direction_vector)
        
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=(x, y))
    
    def update(self):
        self.pos += self.velocity
        if hasattr(self, 'rect'):
            self.rect.center = (int(self.pos.x), int(self.pos.y))
    
    def draw(self, screen):
        if hasattr(self, 'image') and self.image:
            screen.blit(self.image, self.rect)
        else:
            # Fallback: draw a simple line
            end_pos = self.pos + self.velocity.normalize() * 20
            pygame.draw.line(screen, (255, 0, 0), self.pos, end_pos, 3)