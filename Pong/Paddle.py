import pygame
from Constants import *

class Paddle:

    def __init__(self, x, y, width, height):
        self.x = self.initial_x = x
        self.y = self.initial_y = y
        self.width = width
        self.height = height
        self.speed = 8
        self.score = 0
        self.hits = 0

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))
    
    def update(self, up):
        if up == True:
            if (self.y - self.speed) > 0:
                self.y -= self.speed
        else:
            if (self.y + self.speed + self.height) < HEIGHT:
                self.y += self.speed
    
    def reset(self):
        self.x = self.initial_x
        self.y = self.initial_y
        self.hits = 0