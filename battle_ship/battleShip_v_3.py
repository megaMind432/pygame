# Pygame collision ditection
import os
import random

import pygame

# Settings
WIDTH = 600
HEIGHT = 800
FPS = 60

# set-up assets or graphics for the game
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

# Pygame initialize AND create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collision")
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    # Sprite for the Player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((55, 55))
        self.image.fill(MAGENTA)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        # checck for user interaction
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speedx = 5
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speedx = -5
        # update the location
        self.rect.x += self.speedx
        # check edges
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0


class Mob(pygame.sprite.Sprite):
    # sprite for the mobs(Enemy)
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((34, 34))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(1, 8)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.right > WIDTH + 21 or self.rect.left < -21 or self.rect.bottom > HEIGHT + 21:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedx = random.randrange(-3, 3)
            self.speedy = random.randrange(1, 8)


# Sprites Group
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(21):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

# Game-loop
running = True
while running:
    # keep loop running at right speed
    clock.tick(FPS)
    # Process input(events)
    for event in pygame.event.get():
        # check user closing the window
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
