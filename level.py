import pygame
from collectible import Heart, Overhealth
from enemy import Enemy
from interactable import Door, Lever
from platform import Platform

class Level:
    def __init__(self, platforms, enemies, hearts, overhealths, levers, door):
        self.platforms = platforms
        self.enemies = enemies
        self.hearts = hearts
        self.overhealths = overhealths
        self.levers = levers
        self.door = door

def make_test_level():
    platforms = [
        Platform(500,550,500,100),
        Platform(300,550,100,200)
    ]

    enemies = [
        # Enemy(600, 400, "lizard"),
        # Enemy(700, 400, "demon")
    ]

    hearts = [
        Heart(550, 500),
        Heart(650, 500)
    ]

    overhealths = [
        Overhealth(750, 500)
    ]

    levers = [
        Lever(400, 500)
    ]

    door = Door(800, 450)

    return Level(platforms, enemies, hearts, overhealths, levers, door)

def make_level_1():
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

    return Level(platforms, enemies, hearts, overhealths, levers, door)