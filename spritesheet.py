import pygame
import os

class SpriteSheet():
    def __init__(self, image):
        self.sheet = image

    def get_image(self, x, y, width, height, scale):
        image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        image.blit(self.sheet, (0,0), (x, y, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))

        return image
    
    def load_sprite_images(path_to_directory):
        images = {}
        for dirpath, dirnames, filenames in os.walk(path_to_directory):
            for name in filenames:
                if name.endswith('.png'):
                    key = name[:-4]
                    img = pygame.image.load(os.path.join(dirpath, name)).convert_alpha()
                    images[key] = img
        # print(f"Loaded images from {path_to_directory}: {list(images.keys())}")
        return images

    def load_enemy_images(type):
        path_to_directory = f"pygame/assets/enemies/{type}"
        return SpriteSheet.load_sprite_images(path_to_directory)

    def load_collectable_images(type):
        path_to_directory = f"pygame/assets/collectibles/{type}"
        return SpriteSheet.load_sprite_images(path_to_directory)
    
    def load_interactable_images(type):
        path_to_directory = f"pygame/assets/items/{type}"
        return SpriteSheet.load_sprite_images(path_to_directory)
    