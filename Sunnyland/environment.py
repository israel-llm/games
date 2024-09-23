from lib2to3.pgen2.token import GREATER
from constants import*
from images import *
import pygame
import random

class Environment:
    def __init__(self, screen):
        self.screen = screen

        self.grass = GRASS
        self.grass_rect = self.grass.get_rect()
        self.grass_rect.x = 0
        self.grass_rect.y = HEIGHT_SCREEN//2 + 70
        
        self.rock2_coord = []
        self.rock3_coord = []
    
    def draw_background(self, offset):
        self.screen.blit(BACKGROUND, (0, 0))
        self.screen.blit(self.grass, self.grass_rect)
        self.screen.blit(GROUND, (0, HEIGHT_SCREEN//2 + 110))
        for i in range(0,10):
            if len(self.rock3_coord) != 10:
                width = i*120
                height = random.randint(HEIGHT_SCREEN//2 + 110,HEIGHT_SCREEN-40)
                self.rock3_coord.append((width,height))
            self.screen.blit(GROUND_3, self.rock3_coord[i])
        for i in range(0,5):
            if len(self.rock2_coord) != 5:
                width = 40+i*240
                height = random.randint(HEIGHT_SCREEN//2 + 110,HEIGHT_SCREEN-40)
                self.rock2_coord.append((width,height))
            self.screen.blit(GROUND_2, self.rock2_coord[i])
    
    