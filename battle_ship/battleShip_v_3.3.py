# Battle Field v_3.3 with pygame
import os
import random

import pygame

# Set-up assets or graphics for the game
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

# Settings
WIDTH = 400
HEIGHT = 700
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
pygame.display.set_caption("Battle Ship")
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((54, 54))
        self.image.fill(BLUE)
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
        # Update the position of the sprite
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

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Mob(pygame.sprite.Sprite):
    # Sprite for the Enemy
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((34, 34))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-89, -55)
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(5, 8)

    def update(self):
        # update the position for the sprite
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.right > WIDTH + 55 or self.rect.left < -55 or self.rect.bottom > HEIGHT + 55:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-89, -55)
            self.speedx = random.randrange(-3, 3)
            self.speedy = random.randrange(5, 8)


class Bullet(pygame.sprite.Sprite):
    # Sprite for the Bullet
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((12, 21))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()


# Sprite Groups
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    m = Mob()
    mobs.add(m)
    all_sprites.add(mobs)

# Game-loop
running = True
while running:
    # Keep loop running at right speed
    clock.tick(FPS)
    # Process input(events)
    for event in pygame.event.get():
        # Check to see user close the window
        if event.type == pygame.QUIT:
            running = False
        # Shoot the Enemy
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    # update
    all_sprites.update()

    # check to see if a bullet hits a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    # check to see if any of the mobs hits the Player
    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        running = False
    # draw
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # *after* drawing everything flip the display
    pygame.display.flip()

pygame.quit()
