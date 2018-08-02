# Battle Ship collision ditection
import os
import random

import pygame

# Settings
WIDTH = 400
HEIGHT = 600
FPS = 60

# Set-up assets or graphics for the player
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
pygame.display.set_caption("Collision")
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    # Sprite for the player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        self.image.fill(CYAN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT
        self.speedx = 0
        self.speedy = 0

    def update(self):
        self.speedx = 0
        self.speedy = 0
        # track user input for moving the sprites
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speedx = 5
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speedx = -5
        if keystate[pygame.K_UP]:
            self.speedy = -5
        if keystate[pygame.K_DOWN]:
            self.speedy = 5

        # update the location of sprite
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Check edges
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0


class Mob(pygame.sprite.Sprite):
    # Sprite for the Enemy
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((34, 34))
        self.image.fill(MAGENTA)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(1, 8)

    def update(self):
        # update location for mobs
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.right > WIDTH + 55 or self.rect.left < -34 or self.rect.bottom > HEIGHT + 55:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedx = random.randrange(-3, 3)
            self.speedy = random.randrange(1, 8)



# Sprite Groups
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    m = Mob()
    mobs.add(m)
    all_sprites.add(mobs)

# Game-loop
running = True
while running:
    # keep loop running at right speed
    clock.tick(FPS)
    # Input process(events)
    for event in pygame.event.get():
        # Check to see user close the window
        if event.type == pygame.QUIT:
            running = False
    # Update
    all_sprites.update()

    # Check to see if any mob hits the Player
    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        running = False
    # Draw
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # *after* drawing everything flip the display
    pygame.display.flip()
pygame.quit()
