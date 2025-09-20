import random
import pygame
from settings import BULLET_DAMAGE, ENEMY_ATTACK_COOLDOWN, ENEMY_ATTACK_RANGE, ENEMY_DETECTION_RANGE, ENEMY_HEALTH, ENEMY_SPEED, WIDTH

class Enemy:
    def __init__(self,x,y):
        self.pos = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0,0)
        self.health = ENEMY_HEALTH
        self.state = "WANDER"
        self.wander_timer = 0
        self.detection_radius = ENEMY_DETECTION_RANGE
        self.attack_radius = ENEMY_ATTACK_RANGE
        self.attack_cooldown = ENEMY_ATTACK_COOLDOWN
        self.speed = ENEMY_SPEED
    
    def chase_player(self,player):
        direction = (player.pos - self.pos).normalize()
        self.velocity = direction * self.speed
    #wander when player is far away 
    def wander(self, dt):
        self.wander_timer += dt * 1000
        if self.wander_timer > random.randint(2000,4000):
            self.wander_direction = pygame.Vector2(
                random.choice([-1,0,1]),
                random.choice([-1,0,1])
            ).normalize()
            self.wander_timer = 0
        self.velocity = self.wander_direction * (self.speed * 0.5)
    #attack player
    # def attack(self):
    #     if cooldown_ready():
    # def boundaries(self):
    #     self.pos.x = max(50, min(self.pos.x, WIDTH))
    # #taking damage from player
    # def hurt(self):
    #     #TO DO: implement collision method
    #     if collision(player, self):
    #         self.health -= BULLET_DAMAGE

    # def draw(self, screen):

    
