import random
import pygame
from settings import BULLET_DAMAGE, ENEMY_ATTACK_COOLDOWN, ENEMY_ATTACK_RANGE, ENEMY_DETECTION_RANGE, ENEMY_HEALTH, ENEMY_SPEED, WIDTH, HEIGHT, GRAVITY, FLOOR

class Enemy:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.rect = pygame.Rect(x, y, 30, 50)
        self.health = ENEMY_HEALTH
        self.state = "WANDER"  # WANDER, CHASE, ATTACK
        self.wander_timer = 0
        self.detection_radius = ENEMY_DETECTION_RANGE
        self.attack_radius = ENEMY_ATTACK_RANGE
        self.attack_cooldown = ENEMY_ATTACK_COOLDOWN
        self.last_attack = 0
        self.speed = ENEMY_SPEED
        self.jumping = False
        self.is_grounded = False
        self.wander_direction = pygame.Vector2(random.choice([-1, 1]), 0)
        self.facing_right = True
    
    def apply_gravity(self, dt):
        if not self.is_grounded:
            self.velocity.y += GRAVITY * dt + 1
            
        self.pos.y += GRAVITY * dt + 1

        if self.pos.y >= FLOOR:
            self.pos.y = FLOOR
            self.is_grounded = True
            self.jumping = False
            self.velocity.y = 0


    def wander(self, dt):
    # Update wander timer (in seconds)
        self.wander_timer += dt

        # Change direction randomly every 2-4 seconds
        if self.wander_timer >= random.uniform(2.0, 4.0):
            self.wander_direction = pygame.Vector2(random.choice([-1, 1]), 0)
            self.wander_timer = 0

        # Move in wander direction with delta time
        self.velocity.x = self.wander_direction.x * self.speed * 0.5 * dt  # Multiply by dt!

        # Update facing direction
        if self.velocity.x > 0:
            self.facing_right = True
        elif self.velocity.x < 0:
            self.facing_right = False

    def chase_player(self, player, dt):
        direction_x = (player.pos.x - self.pos.x)

        # Move towards player with delta time
        if abs(direction_x) > 10:
            direction = direction_x / abs(direction_x)
            self.velocity.x = direction * self.speed * dt  # Multiply by dt!

            # Update facing direction based on player position
            # if direction_x > 0:
            #     self.facing_right = True
            # else:
            #     self.facing_right = False
        else:
            self.velocity.x = 0

    def attack_player(self, current_time, player):
        # Stop moving when attacking
        self.velocity.x = 0

        # Attack when cooldown is ready
        if current_time - self.last_attack >= self.attack_cooldown:
            player.take_damage()  
            self.last_attack = current_time

    def decide_state(self, player):
        distance_to_player = (player.pos - self.pos).length()
        
        # State transitions
        if distance_to_player <= self.attack_radius:
            self.state = "ATTACK"
        elif distance_to_player <= self.detection_radius:
            self.state = "CHASE"
        else:
            self.state = "WANDER"

    def update(self, player, dt):
        self.apply_gravity(1)

        # Decide which state to be in based on distance to player
        self.decide_state(player)
        current_time = pygame.time.get_ticks()
        # Execute behavior based on current state
        if self.state == "WANDER":
            self.wander(dt)
        elif self.state == "CHASE":
            self.chase_player(player, dt)  # Pass dt here!
        elif self.state == "ATTACK":
            self.attack_player(current_time, player)

        # Boundary checking
        self.pos.x = max(0, min(self.pos.x, WIDTH - self.rect.width))
        self.pos.x += self.velocity.x
        
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

    def take_damage(self):
        self.health -= BULLET_DAMAGE
        return self.health <= 0

    def draw_enemy_healthbar(self, screen):
        healthbar_width = 30
        healthbar_height = 5
        healthbar_x = self.pos.x
        healthbar_y = self.pos.y - 10
        
        health_ratio = self.health / ENEMY_HEALTH
        
        # Background
        background_rect = pygame.Rect(healthbar_x, healthbar_y, healthbar_width, healthbar_height)
        pygame.draw.rect(screen, (50, 50, 50), background_rect)
        
        # Current health
        current_health_width = max(0, healthbar_width * health_ratio)
        if current_health_width > 0:
            health_rect = pygame.Rect(healthbar_x, healthbar_y, current_health_width, healthbar_height)
            
            if health_ratio > 0.6:
                color = (0, 255, 0)
            elif health_ratio > 0.3:
                color = (255, 255, 0)
            else:
                color = (255, 0, 0)
                
            pygame.draw.rect(screen, color, health_rect)

    def draw(self, screen):
        # Draw enemy (will replace with sprites later)
        pygame.draw.rect(screen, (0, 0, 255), self.rect)
        
        # Draw healthbar
        self.draw_enemy_healthbar(screen)
        
        # Debugging - draw state indicator
        state_colors = {
            "WANDER": (0, 255, 0),    # Green
            "CHASE": (255, 255, 0),   # Yellow  
            "ATTACK": (255, 0, 0)     # Red
        }
        pygame.draw.circle(screen, state_colors[self.state], 
                          (int(self.pos.x + 15), int(self.pos.y - 20)), 3)
        
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)  # debugging tool - enemy rect outline
        # pygame.draw.rect(screen, (255, 0, 0), (self.attack_radius, self.pos.y), 2)