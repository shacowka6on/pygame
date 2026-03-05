import pygame

class Level:
    def __init__(self, platforms, enemies, hearts, overhealths, levers, door):
        self.platforms = platforms
        self.enemies = enemies
        self.hearts = hearts
        self.overhealths = overhealths
        self.levers = levers
        self.door = door

    