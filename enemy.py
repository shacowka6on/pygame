from fileinput import filename
import random
import pygame
from settings import *
from spritesheet import SpriteSheet
import os

class Enemy:
    def __init__(self, x, y, type):
        self.pos = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.rect = pygame.Rect(x, y, 60, 80)
        self.health = ENEMY_HEALTH
        self.state = "WANDER"
        self.type = type
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
        self.sprites = self.fill_sprites_dict()
        self.current_animation = "idle"
        self.current_frame = 0
        self.animation_speed = 0.1
        self.animation_timer = 0
    
    def get_animation_offsets(self, facing_right):
        offsets = {}
        if facing_right:
            offsets = {
                "demon": {"x": -90, "y": -150},
                "lizard": {"x": -100, "y": -120}
            }
            # print(f"Facing right x offset: {offsets["x"]}")
        else:
            offsets = {
                "demon": {"x": -140, "y": -150},
                "lizard": {"x": -130, "y": -120}
            }
            # print(f"Facing left x offset: {offsets["x"]}")
        return offsets.get(self.type, {"x": 0, "y": 0})
    
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
        self.wander_timer += dt

        if self.wander_timer >= random.uniform(2.0, 4.0):
            self.wander_direction = pygame.Vector2(random.choice([-1, 1]), 0)
            self.wander_timer = 0

        self.velocity.x = self.wander_direction.x * self.speed * 0.5 * dt

        if self.velocity.x > 0:
            self.facing_right = True
        elif self.velocity.x < 0:
            self.facing_right = False

    def is_facing_right(self, player):
        direction_x = (player.pos.x - self.pos.x)
        if abs(direction_x) > 10:
            direction = direction_x / abs(direction_x)
            if direction > 0:
                self.facing_right = True
            else:
                self.facing_right = False

        return self.facing_right

    def chase_player(self, player, dt):
        direction_x = (player.pos.x - self.pos.x)
       
        if abs(direction_x) > 10:
            direction = direction_x / abs(direction_x)
            self.velocity.x = direction * self.speed * dt
            self.is_facing_right(player)
        else:
            self.velocity.x = 0

    def attack_player(self, current_time, player):
        self.velocity.x = 0
        self.is_facing_right(player)

        if current_time - self.last_attack >= self.attack_cooldown:
            player.take_damage()  
            self.last_attack = current_time

    def decide_state(self, player):
        if self.state == "DEATH":
            return
        if self.state == "HURT" and self.current_animation != "hurt":
            self.state = "WANDER"
            return
            
        distance_to_player = (player.pos - self.pos).length()
        
        if distance_to_player <= self.attack_radius:
            self.state = "ATTACK"
        elif distance_to_player <= self.detection_radius:
            self.state = "CHASE"
        else:
            self.state = "WANDER"

    def update(self, player, dt):
        self.apply_gravity(3)

        if self.state not in ["HURT", "DEATH"]:
            self.decide_state(player)

        current_time = pygame.time.get_ticks()

        new_animation = self.current_animation
        if self.state == "WANDER":
            self.wander(dt)
            new_animation = "walk"
        elif self.state == "CHASE":
            self.chase_player(player, dt)
            new_animation = "walk"
        elif self.state == "ATTACK":
            self.attack_player(current_time, player)
            new_animation = "attack"
        elif self.state == "HURT":
            new_animation = "hurt"
            self.velocity.x = 0
        elif self.state == "DEATH":
            new_animation = "death"
            self.velocity.x = 0
            self.velocity.y = 0
        else:
            new_animation = "idle"

        if new_animation != self.current_animation:
            self.current_animation = new_animation
            self.current_frame = 0
            self.animation_timer = 0

        self.update_animation(dt)

        if self.state != "DEATH":
            self.pos.x = max(0, min(self.pos.x, WIDTH - self.rect.width))
            self.pos.x += self.velocity.x

            self.rect.x = self.pos.x
            self.rect.y = self.pos.y
    
    def take_damage(self):
        self.health -= BULLET_DAMAGE
        if self.health <= 0:
            self.state = "DEATH"
            self.current_frame = 0
            return True
        else:
            if self.state != "DEATH":
                self.state = "HURT"
                self.current_frame = 0
            return False

    def draw_enemy_healthbar(self, screen):
        healthbar_width = 30
        healthbar_height = 5
        healthbar_x = self.pos.x
        healthbar_y = self.pos.y - 10
        
        health_ratio = self.health / ENEMY_HEALTH
        
        background_rect = pygame.Rect(healthbar_x, healthbar_y, healthbar_width, healthbar_height)
        pygame.draw.rect(screen, (50, 50, 50), background_rect)
        
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

    # def load_images(self):
    #     path_to_directory = f"pygame/assets/enemies/{self.type}"
    #     images = {}
    #     for dirpath, dirnames, filenames in os.walk(path_to_directory):
    #         for name in filenames:
    #             if name.endswith('.png'):
    #                 key = name[:-4]
    #                 img = pygame.image.load(os.path.join(dirpath, name)).convert_alpha()
    #                 images[key] = img
    #     return images
    
    def fill_sprites_dict(self):
        # imgs = self.load_images()
        imgs = SpriteSheet.load_images(self.type)

        self.sprites = {"attack": [], "death": [], "hurt": [], "idle": [], "walk": []}

        for filename, image in imgs.items():    
            scaled_img = pygame.transform.scale(image, (256,256))
            if filename.startswith("A"):
                self.sprites["attack"].append(scaled_img)
            elif filename.startswith("D"):
                self.sprites["death"].append(scaled_img)
            elif filename.startswith("H"):
                self.sprites["hurt"].append(scaled_img)
            elif filename.startswith("I"):
                self.sprites["idle"].append(scaled_img)
            elif filename.startswith("W"):
                self.sprites["walk"].append(scaled_img)

        return self.sprites
    
    def update_animation(self, dt):
        self.animation_timer += dt

        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0

            if self.current_animation == "hurt":
                if self.current_frame >= len(self.sprites["hurt"]) - 1:
                    self.state = "WANDER"
                else:
                    self.current_frame += 1

            elif self.current_animation == "death":
                if self.current_frame < len(self.sprites["death"]) - 1:
                    self.current_frame += 1

            else:
                self.current_frame = (self.current_frame + 1) % len(self.sprites[self.current_animation])
    
    def draw(self, screen):
        if self.sprites[self.current_animation]:
            current_image = self.sprites[self.current_animation][self.current_frame]
    
            if not self.facing_right:
                current_image = pygame.transform.flip(current_image, True, False)
    
            animation_offsets = self.get_animation_offsets(self.facing_right)

            offset_x = animation_offsets["x"]
            offset_y = animation_offsets["y"]

            
            draw_x = self.rect.centerx + offset_x
            draw_y = self.rect.centery + offset_y

            # print(f"{self.facing_right}: rectx:{self.rect.centerx} | drawx:{draw_x}/offx:{offset_x}/")
            
            screen.blit(current_image, (draw_x, draw_y))
        
        self.draw_enemy_healthbar(screen)
        
        state_colors = {
            "WANDER": (0, 255, 0),
            "CHASE": (255, 255, 0),  
            "ATTACK": (255, 0, 0),
            "HURT": (10,10,10),
            "DEATH": (0,0,0)
        }
        pygame.draw.circle(screen, state_colors[self.state], 
                          (int(self.pos.x + 15), int(self.pos.y - 20)), 3)
        
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)