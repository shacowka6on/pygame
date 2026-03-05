import pygame
from player import Player
from bullet import Bullet
from enemy import Enemy
from platform import Platform
from collectible import Heart, Overhealth
from interactable import Door, Lever
from level import Level, level_1, test_level
from settings import *
import settings

pygame.init()
pygame.font.init()

class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        self.font = pygame.font.SysFont("Calibri", 30)
        self.current_level = 0
        self.levels = [test_level(), level_1()]
        self.level = self.levels[self.current_level]
        self.player = Player(self.level.player.x, self.level.player.y)

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
        if self.level.door.rect.colliderect(player.rect) and keys[pygame.K_e]:
            self.level.door.on_interact()
            self.level = self.levels[self.current_level + 1]
    
    def interact_with_lever(self, player, keys):
        count = len(self.level.levers)
        for lever in self.level.levers:
            lever.on_interact(player, keys)
            if lever.is_activated:
                count -= 1
        if count == 0:
            self.level.door.is_open = True         

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
        self.player.handle_player_platform_collisions(self.player, self.level.platforms)
        self.player.update_animation()

        for enemy in self.level.enemies:
            enemy.handle_enemy_platform_collisions(self.level.platforms)
            enemy.check_enemy_melee(enemy, self.player)
            enemy.update(self.player, self.dt)
            if enemy.state == "DEATH":
                enemy.remove_enemy(self.level.enemies)

        #get health
        for heart in self.level.hearts:
            heart.collect_heart(self.player, self.level.hearts)
        for overhealth in self.level.overhealths:
             overhealth.collect_overhealth(self.player, self.level.overhealths)

        for bullet in self.player.bullets[:]:
            bullet.update()
            bullet.remove_bullet(self.player.bullets, self.level.enemies, self.level.platforms)

    def draw(self):
        settings.screen.fill(settings.BACKGROUND_COLOR)
        settings.screen.blit(settings.BACKGROUND_IMG, (0,0))

        self.level.door.draw(settings.screen)

        for platform in self.level.platforms:
            platform.draw(settings.screen)

        for enemy in self.level.enemies:
             enemy.draw(settings.screen)

        for heart in self.level.hearts:
            heart.draw(settings.screen)
        
        for overhealth in self.level.overhealths:
            overhealth.draw(settings.screen)

        for lever in self.level.levers:
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