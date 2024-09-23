import pygame
from pygame.locals import *
from Paddle import Paddle
from Ball import Ball
from Constants import *
import sys

pygame.init()

class GameInformation:
    def __init__(self, left_hits, right_hits, left_score, right_score):
        self.left_hits = left_hits
        self.right_hits = right_hits
        self.left_score = left_score
        self.right_score = right_score

class Game:

    def __init__(self, screen):
        
        self.screen = screen

        self.left_paddle = Paddle(10, (HEIGHT-PADD_HEIGHT)//2, PADD_WIDTH, PADD_HEIGHT)
        self.right_paddle = Paddle(WIDTH-PADD_WIDTH-10, (HEIGHT-PADD_HEIGHT)//2, PADD_WIDTH, PADD_HEIGHT)
        self.ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS)
        
    def text(self, text, color, tamaño, posx, posy, center):
        
        myFont = pygame.font.Font(None, tamaño)
        text = myFont.render(text, 0, color)
        text_rect = text.get_rect()
        if center == True:
            text_rect.center = (WIDTH//2), posy
        else:
            text_rect.left = posx
            text_rect.centery = posy
        self.screen.blit(text, text_rect)    

    def draw(self, draw_score=True, draw_hits=False):
        
        self.screen.fill(BLACK)
        pygame.draw.line(self.screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT), 3)
        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        self.ball.draw(self.screen)

        if draw_score:
            self.text(f'{self.left_paddle.score}', WHITE, 50, WIDTH//2 - 150, 50, False)
            self.text(f'{self.right_paddle.score}', WHITE, 50, WIDTH//2 + 150, 50, False)
        if draw_hits:
            self.text(f'{self.left_paddle.hits+self.right_paddle.hits}', WHITE, 50, WIDTH//2, 50, True)    
        
        pygame.display.update() 

    def check_colission(self):
    
        if (self.ball.centery - self.ball.radius) < 0 or (self.ball.centery + self.ball.radius) > HEIGHT:
            self.ball.speed_y *= -1
        
        if self.ball.speed_x < 0:
            if self.ball.centery > self.left_paddle.y and self.ball.centery < (self.left_paddle.y+self.left_paddle.height):   
                if (self.ball.centerx-self.ball.radius) < (self.left_paddle.x+self.left_paddle.width):
                    self.ball.speed_x *= -1
                    self.left_paddle.hits += 1
        else:
            if self.ball.centery > self.right_paddle.y and self.ball.centery < (self.right_paddle.y+self.right_paddle.height):
                if (self.ball.centerx+self.ball.radius) > self.right_paddle.x:
                    self.ball.speed_x *= -1
                    self.right_paddle.hits += 1

    def update(self):

        self.ball.update()
        self.check_colission()

        if self.ball.centerx < 0:
            self.right_paddle.score += 1
            self.ball.reset()
        elif self.ball.centerx > WIDTH:
            self.left_paddle.score += 1
            self.ball.reset()

        game_info = GameInformation(self.left_paddle.hits, self.right_paddle.hits, 
                                    self.left_paddle.score, self.right_paddle.score)
        return game_info

    def reset(self):
        """Resets the entire game."""
        self.ball.reset()
        self.left_paddle.reset()
        self.right_paddle.reset()
        self.left_paddle.score = 0
        self.right_paddle.score = 0

if __name__ == '__main__':
    
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong")
    game = Game(SCREEN)
    reloj = pygame.time.Clock()
    
    run = True
    while run:
        for event in pygame.event.get():      
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        game.draw()

        user_input = pygame.key.get_pressed()
        if user_input[pygame.K_w]:
            game.left_paddle.update(up = True)
        if user_input[pygame.K_s]:
            game.left_paddle.update(up = False)
        if user_input[pygame.K_UP]:
            game.right_paddle.update(up = True)
        if user_input[pygame.K_DOWN]:
            game.right_paddle.update(up = False)

        info = game.update()

        reloj.tick(FPS)