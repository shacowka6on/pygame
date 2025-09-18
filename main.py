import pygame
from player import Player
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

    def update_fps(self):
        fps = str(int(self.clock.get_fps()))
        fps_text = self.font.render(fps, False, ("coral"))
        return fps_text
        
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
        self.player.update()
    
    def draw(self):
        settings.screen.fill(settings.BACKGROUND_COLOR)
        
        self.player.draw(settings.screen)
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        text_surface = self.font.render(f"{mouse_x}, {mouse_y}", False, (0, 0, 0))
        settings.screen.blit(text_surface, (mouse_x + 20, mouse_y))
        settings.screen.blit(self.update_fps(), (10,0))

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