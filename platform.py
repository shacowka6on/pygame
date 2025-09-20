from turtle import title
import pygame

class Platform:
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h

        #3 types of tiles: TOP(1-3), MID(4-6), BOTTOM(7-9) 
        self.tile_type = "TOP"

        self.tile_images = self.load_platform_images()
        self.tile_width, self.tile_height = self.tile_images[0].get_size()
        
        self.tiles_x = (w + self.tile_width - 1) // self.tile_width  
        self.tiles_y = (h + self.tile_height - 1) // self.tile_height 

        self.platform_surface = pygame.Surface((self.tiles_x * self.tile_width, self.tiles_y * self.tile_height), pygame.SRCALPHA)
        self.create_tiled_surface()

    def update(self, x_shift):
        self.rect.x += x_shift

    def load_platform_images(self):
        tile_images = []
        for i in range (1,10):
            img = pygame.image.load(f"pygame/assets/platform/tile{i}.png").convert_alpha()
            tile_images.append(img)
        return tile_images
    
    def draw_tiles(self, x, levelOfDepth):
        if x == 0:
            tile_index = 0 + levelOfDepth
        elif x == (self.tiles_x - 1):
            tile_index = 2 + levelOfDepth
        else:
            tile_index = 1 + levelOfDepth
        return tile_index

    def create_tiled_surface(self):
        for y in range (self.tiles_y):
            for x in range (self.tiles_x):
                if y == 0:
                    levelOfDepth = 0
                elif y == self.tiles_y - 1:
                    levelOfDepth = 6
                else:
                    levelOfDepth = 3

                tile_index = self.draw_tiles(x, levelOfDepth)
                
                print(f"{y} {self.tiles_y}")
                self.platform_surface.blit(self.tile_images[tile_index], (x * self.tile_width, y * self.tile_height))
            
    def draw(self,screen):
        screen.blit(self.platform_surface, (self.x, self.y))
        
