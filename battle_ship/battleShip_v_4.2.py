# Battle Ship Adding Graphics
import random
from os import path

import pygame

# Settings
WIDTH = 400
HEIGHT = 600
FPS = 60

# Colors
WHITE = (233, 233, 233)
BLACK = (0, 0, 0)
RED = (233, 0, 0)
GREEN = (0, 233, 0)
BLUE = (0, 0, 233)
YELLOW = (233, 233, 0)
CYAN = (0, 233, 233)
MAGENTA = (233, 0, 233)

# Pygame initialize and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Graphics")
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((55, 55))
        self.image.fill(MAGENTA)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT
        self.speedx = 0
        self.speedy = 0

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speedx = 8
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speedx = -8
        if keystate[pygame.K_UP]:
            self.speedy = -8
        if keystate[pygame.K_DOWN]:
            self.speedy = 8
        # update the location for the sprite
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Check edges
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT


class Mob(pygame.sprite.Sprite):
    # Sprite for the mob
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((34, 34))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-89, -55)
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(1, 5)

    def __init__(self):
        # update the position for the sprite
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # check to see any of the mobs goes off the display
        if self.rect.right > WIDTH + 55 or self.rect.left < -55 or self.rect.bottom > HEIGHT + 55:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-89, -55)
            self.speedx = random.randrange(-3, 3)
            self.speedy = random.randrange(1, 5)


# Sprite Group
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
# Game-loop
running = True
while running:
    # keep loop running at right speed
    clock.tick(FPS)
    # Input process(events)
    for event in pygame.event.get():
        # check to see if user close the display
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
