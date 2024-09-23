from image_loader import load_player_sprites
import pygame
from os.path import join
import os
from constants import *

PLAYER_IDLE = load_player_sprites(join("assets", "sprites", "player", "idle"), 2)
PLAYER_RUN = load_player_sprites(join("assets", "sprites", "player", "run"), 2)
PLAYER_CROUCH = load_player_sprites(join("assets", "sprites", "player", "crouch"), 2)
PLAYER_CLIMB = load_player_sprites(join("assets", "sprites", "player", "climb"), 2)
PLAYER_HURT = load_player_sprites(join("assets", "sprites", "player", "hurt"), 2)
PLAYER_JUMP = load_player_sprites(join("assets", "sprites", "player", "jump"), 2)

BACKGROUND = pygame.image.load(join(os.getcwd(), "assets", "environment", "layers", "back.png"))
BACKGROUND = pygame.transform.scale(BACKGROUND, (WIDTH_SCREEN, HEIGHT_SCREEN))
MIDDLE = pygame.image.load(join(os.getcwd(), "assets", "environment", "layers", "middle.png"))
MIDDLE = pygame.transform.scale(MIDDLE, (WIDTH_SCREEN//2, 3*HEIGHT_SCREEN//4))
GRASS = pygame.image.load(join(os.getcwd(), "assets", "environment", "layers", "grass.png"))
GRASS = pygame.transform.scale(GRASS, (WIDTH_SCREEN, 40))
GROUND = pygame.image.load(join(os.getcwd(), "assets", "environment", "layers", "ground.png"))
GROUND = pygame.transform.scale(GROUND, (WIDTH_SCREEN, 240))
GROUND_1 = pygame.image.load(join(os.getcwd(), "assets", "environment", "layers", "tierra1.png"))
GROUND_1 = pygame.transform.scale(GROUND_1, (40, 40))
GROUND_2 = pygame.image.load(join(os.getcwd(), "assets", "environment", "layers", "tierra2.png"))
GROUND_2 = pygame.transform.scale(GROUND_2, (40, 45))
GROUND_3 = pygame.image.load(join(os.getcwd(), "assets", "environment", "layers", "tierra3.png"))
GROUND_3 = pygame.transform.scale(GROUND_3, (40, 40))
