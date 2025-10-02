import random
import pygame
from settings import BULLET_DAMAGE, ENEMY_ATTACK_COOLDOWN, ENEMY_ATTACK_RANGE, ENEMY_DETECTION_RANGE, ENEMY_HEALTH, ENEMY_SPEED, WIDTH, HEIGHT, GRAVITY, FLOOR

class Enemy:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.rect = pygame.Rect(x, y, 30, 50)
        self.health = ENEMY_HEALTH
        self.state = "CHASE"
        self.wander_timer = 0
        self.detection_radius = ENEMY_DETECTION_RANGE
        self.attack_radius = ENEMY_ATTACK_RANGE
        self.attack_cooldown = ENEMY_ATTACK_COOLDOWN
        self.speed = ENEMY_SPEED
        self.jumping = False
        self.is_grounded = False
        self.wander_direction = pygame.Vector2(random.choice([-1, 1]), 0)
    
    def apply_gravity(self, dt):
        if not self.is_grounded:
            self.velocity.y += GRAVITY * dt
            
        if self.pos.y >= FLOOR:
            self.pos.y = FLOOR
            self.is_grounded = True
            self.jumping = False
            self.velocity.y = 0

        self.pos.y += GRAVITY * dt
        # print(f"{self.rect.x}{self.rect.y}")
        

    def handle_platform_collisions(self,platforms):
        self.is_grounded = False

    def chase_player(self,player,platforms,dt):
        direction_x = (player.pos.x - self.pos.x)
        if abs(direction_x) > 10:
            direction = direction_x / abs(direction_x)
            self.velocity.x = direction * self.speed
        else:
            self.velocity.x = 0

        self.apply_gravity(dt)
        self.handle_platform_collisions(platforms)

    def update(self, player, platforms, dt):
        self.apply_gravity(1)
        distance_to_player = (player.pos - self.pos).length()
        if distance_to_player <= 1280:
            self.state = "CHASE"
            self.chase_player(player,platforms,dt)
        self.pos.x = max(0, min(self.pos.x, WIDTH - self.rect.width))
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

    
    
    def draw(self, screen):
        # Draw enemy as red square
        pygame.draw.rect(screen, (0, 0, 255), self.rect)
        
        pygame.draw.rect(screen, (255,0,0), self.rect, 2) #debugging tool
        # Optional: Draw state indicator
        # state_color = (255, 255, 0) if self.state == "CHASE" else (0, 255, 0)
        # pygame.draw.circle(screen, state_color, (int(self.pos.x + 15), int(self.pos.y - 10)), 5)