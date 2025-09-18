import pygame
from settings import *
from bullet import Bullet
from spritesheet import SpriteSheet

class Player:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.facing_right = True
        self.jumping = False
        self.bullets = []
        
        self.last_animation_update = 0
        self.last_attack = 0
        self.frame = 0
        self.action = 0  # 0 idle, 1 jump, 2 fall, 3 run
        
        self.sprite_sheet_image = pygame.image.load('pygame/assets/blastalot-wings-alpha.png').convert_alpha()
        self.sprite_sheet = SpriteSheet(self.sprite_sheet_image)
        self.animation_list = self.load_animations()
    
    def load_animations(self):
        animation_list = []
        animation_steps = [1, 1, 1, 6]  # idle, jump, fall, run
        step_counter = 0
        
        for animation in animation_steps:
            temp_img_list = []
            for _ in range(animation):
                x = step_counter * FRAME_WIDTH
                y = 0 
                temp_img_list.append(self.sprite_sheet.get_image(
                    x, y, FRAME_WIDTH, FRAME_HEIGHT, SCALE
                ))
                step_counter += 1
            animation_list.append(temp_img_list)
        
        return animation_list
    
    def handle_movement_input(self, keys, dt):
        self.velocity.x = 0
        if keys[pygame.K_a]:
            self.velocity.x = -MOVE_SPEED * dt
            self.facing_right = False
        if keys[pygame.K_d]:
            self.velocity.x = MOVE_SPEED * dt
            self.facing_right = True
            
        if keys[pygame.K_SPACE] and not self.jumping:
            self.jump()
            
        self.pos.x += self.velocity.x
        self.pos.y += self.velocity.y
        
        if self.jumping:
            self.velocity.y += GRAVITY
            if self.pos.y >= FLOOR: 
                self.pos.y = FLOOR
                self.jumping = False
                self.velocity.y = 0
    
    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.velocity.y = -JUMP_FORCE
    
    def handle_shoot_input(self, target_x, target_y):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack >= SHOOT_COOLDOWN:
            bullet = Bullet(self.pos.x, self.pos.y, target_x, target_y)
            self.bullets.append(bullet)
            self.last_attack = current_time
    
    def update(self):
        for bullet in self.bullets[:]:
            bullet.update()
            if (bullet.pos.x < 0 or bullet.pos.x > WIDTH or 
                bullet.pos.y < 0 or bullet.pos.y > HEIGHT):
                self.bullets.remove(bullet)
        
        self.update_animation()
    
    def update_animation(self):
        current_time = pygame.time.get_ticks()
        
        new_action = self.action
        if self.jumping:
            if self.velocity.y > 0:
                new_action = 2  # jumping 
            else:
                new_action = 1  # falling down
        elif self.velocity.x != 0:
            new_action = 3  # running
        else:
            new_action = 0  # idle
        
        if new_action != self.action:
            self.action = new_action
            self.frame = 0
            self.last_animation_update = current_time
            
        #reset to frame 0 when changing action or the game crashes
        if self.action >= len(self.animation_list):
            self.action = 0
        if self.frame >= len(self.animation_list[self.action]):
            self.frame = 0 

        if current_time - self.last_animation_update >= ANIMATION_COOLDOWN:
            self.frame = (self.frame + 1) % len(self.animation_list[self.action])
            self.last_animation_update = current_time
    
    def draw(self, screen):
        for bullet in self.bullets:
            bullet.draw(screen)
        
        frame_img = self.animation_list[self.action][self.frame]
        if not self.facing_right:
            frame_img = pygame.transform.flip(frame_img, True, False)
        
        frame_rect = frame_img.get_rect(center=(self.pos.x, self.pos.y))
        screen.blit(frame_img, frame_rect)