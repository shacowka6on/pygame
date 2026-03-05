import pygame
from spritesheet import SpriteSheet

class Interactable:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.rect = pygame.Rect(x, y, 0, 0)
        self.sprite = self.load_sprites()

    def load_sprites(self):
        raise NotImplementedError("Subclasses must implement this method")
    
    def on_interact(self):
        raise NotImplementedError("Subclasses must implement this method")
    
    def draw(self, screen):
        screen.blit(self.image, self.pos)
        pygame.draw.rect(screen, (0,0,255), self.rect, 2)#debugging tool    

class Lever(Interactable):
    def __init__(self, x, y):
        super().__init__(x-20, y-20)
        self.rect = pygame.Rect(x, y, 35, 35)
        self.is_activated = False

    def load_sprites(self):
        images_dict = SpriteSheet.load_interactable_images("lever")
        return [images_dict[key] for key in sorted(images_dict.keys())]
    
    def on_interact(self, player, keys):
        # print(player.rect.colliderect(self.rect))
        if player.rect.colliderect(self.rect) and keys[pygame.K_e]:
            self.is_activated = True
        
    def draw(self, screen):
        if(self.is_activated):
            self.image = self.sprite[0]
        else:
            self.image = self.sprite[1]

        screen.blit(self.image, self.pos)
        pygame.draw.rect(screen, (0,0,255), self.rect, 2) #debugging tool   

    
class Door(Interactable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rect = pygame.Rect(x, y, 70, 70)
        self.is_open = False

    def load_sprites(self):
        images_dict = SpriteSheet.load_interactable_images("door")
        return [images_dict[key] for key in sorted(images_dict.keys())]
    
    def on_interact(self):
        if self.is_open:
            print("Door is open, player can pass through")
    
    def draw(self, screen):
        if(self.is_open):
            self.image = self.sprite[1]
        else:
            self.image = self.sprite[0]

        screen.blit(self.image, self.pos)
        pygame.draw.rect(screen, (0,0,255), self.rect, 2) #debugging tool