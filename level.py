import pygame
from collectible import Heart, Overhealth
from enemy import Enemy
from interactable import Door, Lever
from platform import Platform
from player import Player
from settings import FLOOR, WIDTH

class Level:
    def __init__(self, player_pos, platforms, enemies, hearts, overhealths, levers, door):
        self.player = pygame.Vector2(player_pos.pos.x, player_pos.pos.y)
        self.platforms = platforms
        self.enemies = enemies
        self.hearts = hearts
        self.overhealths = overhealths
        self.levers = levers
        self.door = door

def test_level():
    player = Player(100,500)
    
    platforms = [
        Platform(0,FLOOR,WIDTH, 130),
    ]

    enemies = [
        Enemy(600, 400, "lizard"),
        Enemy(700, 400, "demon")
    ]

    hearts = [
        Heart(550, 500),
        Heart(650, 500)
    ]

    overhealths = [
        Overhealth(750, 500)
    ]

    levers = [
        Lever(145, 530)
    ]

    door = Door(600, 500)

    return Level(player, platforms, enemies, hearts, overhealths, levers, door)

def level_1():
    player = Player(100,500)

    platforms = [
        Platform(500,550,500,100),
        Platform(300,550,100,200),
        Platform(200,100,400,80),
        Platform(0,550,800, 130)
    ]

    enemies = [
        Enemy(200,200, "lizard"),
        Enemy(400,400, "demon")
    ]

    hearts = [
        Heart(140,650)
    ]

    overhealths = [
        Overhealth(300, 500)
    ]

    levers = [
        Lever(360, 530),
        Lever(600, 530)
    ]

    door = Door(700, 500)

    return Level(player, platforms, enemies, hearts, overhealths, levers, door)