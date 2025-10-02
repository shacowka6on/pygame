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

    def chase_player(self,player):
        direction_x = (player.pos.x - self.pos.x)
        if abs(direction_x) > 10:
            direction = direction_x / abs(direction_x)
            self.velocity.x = direction * self.speed
        else:
            self.velocity.x = 0

    def take_damage(self):
        self.health -= BULLET_DAMAGE
        return self.health <= 0

    def update(self, player):
        self.apply_gravity(1)
        distance_to_player = (player.pos - self.pos).length()

        if distance_to_player <= WIDTH:
            self.state = "CHASE"
            self.chase_player(player)

        self.pos.x = max(0, min(self.pos.x, WIDTH - self.rect.width))

        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

    def draw_enemy_healthbar(self, screen):
        # Healthbar dimensions
        healthbar_width = 30
        healthbar_height = 5
        healthbar_x = self.pos.x
        healthbar_y = self.pos.y - 10  # Position above enemy

        # Calculate current health percentage
        health_ratio = self.health / ENEMY_HEALTH

        # Background (empty health)
        background_rect = pygame.Rect(healthbar_x, healthbar_y, healthbar_width, healthbar_height)

        # Foreground (current health)
        current_health_width = max(0, healthbar_width * health_ratio)
        if current_health_width > 0:
            health_rect = pygame.Rect(healthbar_x, healthbar_y, current_health_width, healthbar_height)

            # Color based on health percentage
            if health_ratio >= 0.5:
                color = (0, 255, 0)  # Green when healthy
            elif health_ratio >= 0.3:
                color = (255, 255, 0)  # Yellow when medium health
            else:
                color = (255, 0, 0)  # Red when low health

            pygame.draw.rect(screen, color, health_rect)
    
    def draw(self, screen):
        # Draw enemy as red square
        pygame.draw.rect(screen, (0, 0, 255), self.rect)
        self.draw_enemy_healthbar(screen)
        pygame.draw.rect(screen, (255,0,0), self.rect, 2) #debugging tool
        # Optional: Draw state indicator
        # state_color = (255, 255, 0) if self.state == "CHASE" else (0, 255, 0)
        # pygame.draw.circle(screen, state_color, (int(self.pos.x + 15), int(self.pos.y - 10)), 5)