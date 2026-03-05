import pygame
from settings import *

class Bullet:
    def __init__(self, x, y, target_x, target_y):
        self.pos = pygame.Vector2(x, y)
        self.rect = pygame.Rect(x,y,10,10)
        direction = pygame.Vector2(target_x - x, target_y - y).normalize()
        self.velocity = direction * BULLET_SPEED

        self.original_image = pygame.image.load('pygame/assets/laserBullet.png').convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (15, 20))
        
        direction_vector = pygame.math.Vector2(target_x - x, target_y - y)
        angle = direction_vector.angle_to(pygame.math.Vector2(0, -1))
        
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=(10, 10))
        
    
    def update(self):
        self.pos += self.velocity
        if hasattr(self, 'rect'):
            self.rect.center = (int(self.pos.x), int(self.pos.y))
        
    def remove_bullet(self, bullets, enemies, platforms):
        for bullet in bullets[:]:
            bullet.update()
            if (bullet.pos.x < 0 or bullet.pos.x > WIDTH or 
                bullet.pos.y < 0 or bullet.pos.y > HEIGHT):
                bullets.remove(bullet)
            for enemy in enemies[:]:
                if bullet.did_bullet_collide(enemy.rect):
                    # Trigger hurt state and take damage
                    enemy_died = enemy.take_damage()
                    bullets.remove(bullet)

                    if enemy_died:
                        # Enemy will handle death animation in its update
                        pass
                    break
            for platform in platforms:
                if bullet.did_bullet_collide(platform.rect):
                    bullets.remove(bullet)

    def update_bullets(self,player,level):
        bullets_to_remove = []

        # for bullet in player.bullets[:]:
            # for enemy in level.enemies[:]:
            #     if bullet.did_bullet_collide(enemy.rect):
            #         # Trigger hurt state and take damage
            #         enemy_died = enemy.take_damage()
            #         bullets_to_remove.append(bullet)

            #         if enemy_died:
            #             # Enemy will handle death animation in its update
            #             pass
            #         break

        #     for platform in level.platforms:
        #         if bullet.did_bullet_collide(platform.rect):
        #             bullets_to_remove.append(bullet)

        # for bullet in bullets_to_remove:
        #     if bullet in player.bullets:
        #         player.bullets.remove(bullet)

        # Remove dead enemies after death animation completes
        for enemy in level.enemies[:]:
            if enemy.health <= 0 and enemy.current_animation == "death" and enemy.current_frame >= len(enemy.sprites["death"]) - 1:
                level.enemies.remove(enemy)

    def did_bullet_collide(self, obj_rect):
        return self.rect.colliderect(obj_rect)
    
    def draw(self, screen):
        if hasattr(self, 'image') and self.image:
            screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (0,0,255), self.rect, 2) #debugging tool
        