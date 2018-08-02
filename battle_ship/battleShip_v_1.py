# Enemy sprite
import os
import random

import pygame

# Settings
WIDTH = 500
HEIGHT = 800
FPS = 60

# setting up the assets img_folder
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

# Colors
WHITE = (233, 233, 233)
BLACK = (0, 0, 0)
RED = (233, 0, 0)
GREEN = (0, 233, 0)
BLUE = (0, 0, 233)
YELLOW = (233, 233, 0)
CYAN = (0, 233, 233)
MAGENTA = (233, 0, 233)

# pygame initialize and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enemy Sprite")
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((89, 55))
        self.image.fill(MAGENTA)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        # user input to move the player sprite
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speedx = 5
        self.rect.x += self.speedx
        # check edge
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0


# Sprite Groups
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# Game-loop
running = True
while running:
    # check for running loop at right speed
    clock.tick(FPS)
    # Input process (event)
    for event in pygame.event.get():
        # check for user closing the window
        if event.type == pygame.QUIT:
            running = False
    # update
    all_sprites.update()

    # draw
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # *after* drawing everything flip the display
    pygame.display.flip()

pygame.quit()
