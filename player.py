import pygame
from settings import *
from bullet import Bullet
from spritesheet import SpriteSheet

class Player:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.health = 80
        self.facing_right = True
        self.jumping = False
        self.last_jump_time = 0
        self.jumping_cooldown = 500
        self.is_grounded = True
        self.bullets = []
        self.rect = pygame.Rect(x,y,35,60)
        
        self.last_animation_update = 0
        self.last_attack = 0
        self.frame = 0
        self.action = 0  # 0 idle, 1 jump, 2 fall, 3 run
        
        self.sprite_sheet_image = pygame.image.load('pygame/assets/blastalot-wings-alpha.png').convert_alpha()
        self.sprite_sheet = SpriteSheet(self.sprite_sheet_image)
        self.animation_list = self.load_animations()
    
    def draw_player_health(self):
        font = pygame.font.SysFont("Calibri", 30)
        text = font.render(f"Health: {self.health}", False, "Red")
        return text


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
    
    def handle_interaction(self, keys, interactables):
        for interactable in interactables:
            if self.rect.colliderect(interactable.rect) and keys[pygame.K_e]:
                interactable.on_interact(self)

    def handle_movement_input(self, keys, dt):
        self.velocity.x = 0
        if keys[pygame.K_a]:
            self.velocity.x = -MOVE_SPEED * dt
            self.facing_right = False
        if keys[pygame.K_d]:
            self.velocity.x = MOVE_SPEED * dt
            self.facing_right = True
        
        self.check_for_ground()

        # if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        #     self.jump()
            
        self.pos.x += self.velocity.x
        self.pos.y += self.velocity.y
        
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
            
    
    def jump(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_jump_time < self.jumping_cooldown:
            return False
        
        #if player is moving give him a boost or the jump is shorter
        # boost = 0
        # if keys[pygame.K_a] or keys[pygame.K_d]:
        #     boost = -5 

        if not self.jumping:
            self.last_jump_time = current_time
            self.jumping = True
            self.velocity.y = -JUMP_FORCE 
        elif self.jumping:
            self.velocity.y += GRAVITY
            if self.pos.y >= FLOOR: 
                self.pos.y = FLOOR
                self.jumping = False
                self.velocity.y = 0
    
    def check_for_ground(self):
        if not self.is_grounded:
            self.velocity.y += GRAVITY
            # print(self.action)

    def take_damage(self):
        self.health -= ENEMY_DAMAGE
        return self.health <= 0
    
    def handle_shoot_input(self, target_x, target_y):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack >= SHOOT_COOLDOWN:
            #added a little offset to x and y because bullets spawn from the top of the player 
            bullet = Bullet(self.pos.x + 15, self.pos.y + 30, target_x, target_y)
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
                new_action = 1  # jumping 
        if self.velocity.y > 1:
            new_action = 2  # falling down
        elif self.velocity.x != 0:
            new_action = 3  # running
        else:
            new_action = 0  # idle
        
        if new_action != self.action:
            self.action = new_action
            self.frame = 0
            self.last_animation_update = current_time
            
        #reset to frame 0 when changing action or the game crashes
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
        
        frame_rect = frame_img.get_rect(center=(self.pos.x + 20, self.pos.y + 20))
        screen.blit(frame_img, frame_rect)

        screen.blit(self.draw_player_health(), (10,0))

        pygame.draw.rect(screen, (0,255,0), self.rect, 2) #debugging tool