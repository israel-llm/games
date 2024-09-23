import pygame
import random
from Constants import *

class Ball:

    def __init__(self, x, y, radius):
        self.centerx = self.initial_x = x
        self.centery = self.initial_y = y
        self.radius = radius
        self.speed_x = 5*random.choice([-1,1])
        self.speed_y = 5*random.choice([-1,1])
    
    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (self.centerx, self.centery), self.radius)
    
    def update(self):
        self.centerx += self.speed_x
        self.centery += self.speed_y
    
    def reset(self):
        self.centerx = self.initial_x
        self.centery = self.initial_y
        self.speed_y = 5*random.choice([-1,1])
        self.speed_x *= -1