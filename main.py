import pygame
from player import Player
from enemy import Enemy
from platform import Platform 
from collectible import Collectible
import settings

pygame.init()
pygame.font.init()

class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        self.player = Player(100, settings.FLOOR)
        self.font = pygame.font.SysFont("Calibri", 30)
        self.platforms = [
            #        x   y   w   h
            Platform(700,600,128,64), #level 1 depth
            Platform(300,300,200,300),
            Platform(0,settings.FLOOR,settings.WIDTH, 130), #main bottom platform
            
        ]
        self.enemies = [
            Enemy(200,200, "lizard"),
            Enemy(300,400, "demon")
        ]
        self.collectibles = [
            Collectible(100,100,"heart")
        ]

    def update_fps(self):
        fps = str(int(self.clock.get_fps()))
        fps_text = self.font.render(fps, False, ("green"))
        return fps_text
    
    def handle_bullet_collisions(self):
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
                
    def handle_enemy_collide_w_player(self):
        current_time = pygame.time.get_ticks()
        for enemy in self.enemies:
            if enemy.rect.colliderect(self.player.rect):
                enemy.attack_player(current_time, self.player)
                    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.player.handle_shoot_input(mouse_x, mouse_y)
    
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
            # print(enemy.load_animations())
            enemy.update(self.player, self.dt)

        for collectible in self.collectibles:
            # collectible.draw(settings.screen)
            # collectible.animate(self.dt)
            settings.screen.blit(collectible.draw(), (200,200))

        self.handle_enemy_collide_w_player()
        self.handle_bullet_collisions()
        self.player.update()
    
    def draw(self):
        settings.screen.fill(settings.BACKGROUND_COLOR)  
        settings.screen.blit(settings.BACKGROUND_IMG, (0,0))
        
        for platform in self.platforms:
            platform.draw(settings.screen)
        
        self.player.draw(settings.screen)

        for enemy in self.enemies:
            enemy.draw(settings.screen)
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        text_surface = self.font.render(f"{mouse_x}, {mouse_y}", False, "cyan")
        settings.screen.blit(text_surface, (mouse_x + 20, mouse_y))
        settings.screen.blit(self.update_fps(), (settings.WIDTH - 50,0))

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