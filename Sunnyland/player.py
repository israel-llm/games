from images import *
import pygame
from constants import *

class Player:
    ACTIONS = {
        "idle": PLAYER_IDLE,
        "run": PLAYER_RUN,
        "crouch": PLAYER_CROUCH,
        "climb": PLAYER_CLIMB,
        "hurt": PLAYER_HURT,
        "jump": PLAYER_JUMP
    }

    def __init__(self, x, y, direction):

        self.x = x
        self.y = y

        self.direction = direction
        self.img = None
        self.rect = None
        self.counter = 0
        self.action = "idle"
        self.animation_count = 0
        self.frame_duration = 5

        self.jumping = False
        self.falling = False
        self.in_stair = False
        self.start_y = self.y

        self.CLIMB_VEL = 3
        self.RUN_VEL = 5
        self.GRAVITY = 10
        self.JUMP_VEL_Y = 18
        self.JUMP_VEL_X = 0

        self.offset = 0
        self.limit = None
        self.change_direction = False

    def draw(self, screen):
  
        action = self.ACTIONS[self.action][self.direction]

        if self.counter >= len(action):
            self.counter = 0
            
        self.img = action[self.counter]
        self.rect = self.img.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        screen.blit(self.img, (self.x, self.y))
        #pygame.draw.rect(screen, (0,0,0), (self.x, self.y, self.img.get_width(), self.img.get_height()), 2)  
            
        if self.jumping == True and self.falling == True:
            self.counter = 1
        else:
            self.animation_count += 1
            if self.animation_count % self.frame_duration == 0:
                self.counter += 1
                self.animation_count = 0

    def move(self, user_input):
        if not self.jumping:
            if user_input[pygame.K_SPACE] and user_input[pygame.K_d]:
                self.jump(on_site=False, left=False)
            elif user_input[pygame.K_SPACE] and user_input[pygame.K_a]:
                self.jump(on_site=False, left=True)
            elif user_input[pygame.K_s]:
                self.crouch()
            elif user_input[pygame.K_e]:
                self.hurt()
            elif user_input[pygame.K_s] and self.in_stair:
                self.climb(up=False)
            elif user_input[pygame.K_w]: #and self.in_stair:
                self.climb(up=True)
            elif user_input[pygame.K_SPACE]:
                self.jump()
            elif user_input[pygame.K_d]: #and self.blocked_direction != "right":
                self.run(left=False)
            elif user_input[pygame.K_a]: #and self.blocked_direction != "left":
                self.run(left=True)
            else:
                self.idle()
        else:
            if user_input[pygame.K_d]:
                self.JUMP_VEL_X = +5
                self.direction = "right"
            elif user_input[pygame.K_a]:
                self.JUMP_VEL_X = -5
                self.direction = "left"
            self.jump()

    def idle(self):
        self.action = "idle"
        self.frame_duration = 8

    def run(self, left):
        self.action = "run"
        self.frame_duration = 5

        if left:
            self.direction = "left"
            self.RUN_VEL = -5
        else:
            self.direction = "right"
            self.RUN_VEL = +5
        
        if self.limit == "right":
            if self.offset + self.RUN_VEL < WIDTH_SCREEN:
                self.offset += self.RUN_VEL
        elif self.limit == "left":
            if self.offset + self.RUN_VEL > 0:
                self.offset += self.RUN_VEL
        else:
            self.limit = None
            self.x += self.RUN_VEL
        
    
    def climb(self, up):
        self.action = "climb"
        self.start_y = self.y
        self.frame_duration = 10

        if up:
            self.CLIMB_VEL = -3
        else:
            self.CLIMB_VEL = +3

        self.y += self.CLIMB_VEL
    
    def jump(self, on_site=True, left=True):
        
        if not self.jumping:
            self.action = "jump"
            self.jumping = True
            self.start_y = self.y
            self.JUMP_VEL_Y = +18

            if on_site:
                self.JUMP_VEL_X = 0
            else:
                if left:
                    self.JUMP_VEL_X = -5
                else:
                    self.JUMP_VEL_X = +5

        if self.limit == "right":
            if self.offset + self.JUMP_VEL_X < WIDTH_SCREEN:
                self.offset += self.JUMP_VEL_X
        elif self.limit == "left":
            if self.offset + self.JUMP_VEL_X > 0:
                self.offset += self.JUMP_VEL_X
        else:
            self.limit = None
            self.x += self.JUMP_VEL_X
        
        self.y -= self.JUMP_VEL_Y

        if self.y == self.start_y:
            self.jumping = False
            self.falling = False
            self.counter = 0
        else:    
            self.JUMP_VEL_Y -= 1
            if self.JUMP_VEL_Y < 0:
                self.falling = True
        

    def hurt(self):
        self.action = "hurt"
        self.frame_duration = 7

    def crouch(self):
        self.action = "crouch"
        self.frame_duration = 9

    def check_limits(self):
        if self.x <= MOVEMENT_BORDER_LEFT:
            self.limit = "left"
            if self.direction == "right":
                self.limit = None
        elif self.x + self.img.get_width() >= MOVEMENT_BORDER_RIGHT:
            self.limit = "right"
            if self.direction == "left":
                self.limit = None
        else:
            self.limit = None
    
    def check_collision(self, grass_rect):
        if not self.jumping:
            if not self.rect.colliderect(grass_rect):
                self.y += self.GRAVITY
