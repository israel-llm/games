import pygame
from pygame.locals import *   #CONSTANTES DE PYGAME
import sys
from images import *
from constants import *
from player import Player
from environment import Environment

pygame.init()

def main():

    clock = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
    pygame.display.set_caption("Sunnyland")
    player = Player(WIDTH_SCREEN//2, HEIGHT_SCREEN//2-99, "right")
    environment = Environment(SCREEN)

    while True:
        
        environment.draw_background(player.offset)

        for event in pygame.event.get():                            #Revisa en cada lazo si se quiere cerrar la ventana
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        user_input = pygame.key.get_pressed()
        player.move(user_input)
        player.draw(SCREEN)
        player.check_limits()
        player.check_collision(environment.grass_rect)    
        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()