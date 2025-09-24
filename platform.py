import pygame

class Platform:
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y

        self.tile_images = self.load_platform_images()
        self.tile_width, self.tile_height = self.tile_images[0].get_size()
        
        self.tiles_x = (w + self.tile_width - 1) // self.tile_width  
        self.tiles_y = (h + self.tile_height - 1) // self.tile_height 
        
        self.width = self.tiles_x * self.tile_width
        self.height = self.tiles_y * self.tile_height
        self.rect = pygame.Rect(x,y,self.width,self.height)
       
        self.platform_surface = pygame.Surface((self.tiles_x * self.tile_width, self.tiles_y * self.tile_height), pygame.SRCALPHA)
        self.create_tiled_surface()

    def update(self, x_shift):
        self.rect.x += x_shift

    def check_collision(self, player_rect):
        return self.rect.colliderect(player_rect)
    
    def get_collision_direction(self, player_rect):
        if not self.check_collision(player_rect):
            return None
        
        dx1 = player_rect.right - self.rect.left
        dx2 = self.rect.right - player_rect.left
        dy1 = player_rect.bottom - self.rect.top
        dy2 = self.rect.bottom - player_rect.top

        min_overlap = min(dx1,dx2,dy1,dy2)

        if min_overlap == dx1:
            return "left"
        elif min_overlap == dx2:
            return "right"
        elif min_overlap == dy1:
            return "top"
        elif min_overlap == dy2:
            return "bottom"
        
        return None
    
    def handle_collision(self, player, player_rect):
        direction = self.get_collision_direction(player_rect)
        print(f"Player coords: {player.rect.x, player.rect.y} collision direction {direction}")
        if direction == "top":
            player_rect.bottom = self.rect.top
            player.pos.y = player_rect.y
            player.velocity.y = 0
            return True
        elif direction == "bottom":
            player_rect.top = self.rect.bottom
            player.pos.y = player_rect.y
            player.velocity.y = 0
        elif direction == "left":
            player_rect.right = self.rect.left
            player.pos.x = player_rect.x
        elif direction == "right":
            player_rect.left = self.rect.right
            player.pos.x = player_rect.x

        return False

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

                self.platform_surface.blit(self.tile_images[tile_index], (x * self.tile_width, y * self.tile_height))
            
    def draw(self,screen):
        screen.blit(self.platform_surface, (self.x, self.y))
        # pygame.draw.rect(screen, (255,0,0), self.rect, 2) debugging tool
        
