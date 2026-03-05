import pygame
from player import Player
from enemy import Enemy
from platform import Platform
from collectible import Heart, Overhealth
from interactable import Door, Lever
from settings import *
import settings

pygame.init()
pygame.font.init()

class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        self.player = Player(520, 50)
        self.font = pygame.font.SysFont("Calibri", 30)
        self.platforms = [
            #        x   y   w   h
            # Platform(700,600,128,64), #level 1 depth
            Platform(500,550,500,100),
            Platform(300,550,100,200),
            Platform(200,100,400,80),
            Platform(0,settings.FLOOR,settings.WIDTH, 130), #main bottom platform

        ]
        self.enemies = [
             Enemy(200,200, "lizard"),
             Enemy(200,200, "lizard"),
             Enemy(400,400, "demon"),
            Enemy(400,400, "demon"),
        ]
        self.hearts = [
            Heart(140,650)
        ]
        self.overhealths = [
            Overhealth(300, 500)
        ]
        self.door = Door(700, 500)
        # self.lever = Lever(360, 530)
        self.levers = [
            Lever(360, 530),
            Lever(600, 530)
        ]

    def get_fps_text(self):
        fps = str(int(self.clock.get_fps()))
        fps_text = self.font.render(fps, False, ("green"))
        return fps_text
    
    def draw_fps(self, screen):
        fps_text = self.get_fps_text()
        screen.blit(fps_text, (settings.WIDTH - 50,0))

    def draw_cursor_info(self, screen):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        text_surface = self.font.render(f"{mouse_x}, {mouse_y}", False, "cyan")
        screen.blit(text_surface, (mouse_x + 20, mouse_y))
    
    def interact_with_door(self, player, keys):
        if self.door.rect.colliderect(player.rect) and keys[pygame.K_e]:
            self.door.on_interact()
    
    def interact_with_lever(self, player, keys):
        count = len(self.levers)
        for lever in self.levers:
            lever.on_interact(player, keys)
            if lever.is_activated:
                count -= 1
        if count == 0:
            self.door.is_open = True

    def collect_heart(self):
        for heart in self.hearts[:]:
            if heart.check_collision(self.player.rect) and self.player.health < 100:
                self.hearts.remove(heart)
                heart.on_collect(self.player)

    def collect_overhealth(self):
        for overhealth in self.overhealths[:]:
            if overhealth.check_collision(self.player.rect):
                self.overhealths.remove(overhealth)
                overhealth.on_collect(self.player)
            
    def update_bullets(self):
        bullets_to_remove = []

        for bullet in self.player.bullets[:]:
            for enemy in self.enemies[:]:
                if bullet.did_bullet_collide(enemy.rect):
                    # Trigger hurt state and take damage
                    enemy_died = enemy.take_damage()
                    bullets_to_remove.append(bullet)

                    if enemy_died:
                        # Enemy will handle death animation in its update
                        pass
                    break

            for platform in self.platforms:
                if bullet.did_bullet_collide(platform.rect):
                    bullets_to_remove.append(bullet)

        for bullet in bullets_to_remove:
            if bullet in self.player.bullets:
                self.player.bullets.remove(bullet)

        # Remove dead enemies after death animation completes
        for enemy in self.enemies[:]:
            if enemy.health <= 0 and enemy.current_animation == "death" and enemy.current_frame >= len(enemy.sprites["death"]) - 1:
                self.enemies.remove(enemy)

    def check_enemy_melee(self):
        for enemy in self.enemies:
            if enemy.rect.colliderect(self.player.rect):    
                enemy.attack_player(self.player)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.player.handle_shoot_input(mouse_x, mouse_y)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.interact_with_lever(self.player, pygame.key.get_pressed())
                    self.interact_with_door(self.player, pygame.key.get_pressed())

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.handle_movement_input(keys, self.dt)
        self.player.is_grounded = False

        for platform in self.platforms:
            if platform.check_collision(self.player.rect):
                is_grounded = platform.handle_collision(self.player, self.player.rect)
                if is_grounded:
                    self.player.is_grounded = True
                    self.player.jumping = False

        for enemy in self.enemies:
            for platform in self.platforms:
                if platform.check_collision(enemy.rect):
                    is_grounded = platform.handle_collision(enemy, enemy.rect)
                    if is_grounded:
                        enemy.is_grounded = True
                        enemy.jumping = False
            enemy.update(self.player, self.dt)

        self.collect_heart()
        self.collect_overhealth()
        self.check_enemy_melee()
        self.update_bullets()
        self.player.update()

    def draw(self):
        settings.screen.fill(settings.BACKGROUND_COLOR)
        settings.screen.blit(settings.BACKGROUND_IMG, (0,0))

        for platform in self.platforms:
            platform.draw(settings.screen)

        for enemy in self.enemies:
             enemy.draw(settings.screen)

        for heart in self.hearts:
            heart.draw(settings.screen)
        
        for overhealth in self.overhealths:
            overhealth.draw(settings.screen)

        self.door.draw(settings.screen)
        for lever in self.levers:
            lever.draw(settings.screen)
        self.player.draw(settings.screen)

        self.draw_fps(settings.screen)
        self.draw_cursor_info(settings.screen)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.dt = self.clock.tick(60) / 1000

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()