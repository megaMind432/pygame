# Battle Ship adding graphics
import random
from os import path

import pygame

# get image directory from os
img_dir = path.join(path.dirname(__file__), 'img')

# Settings
WIDTH = 500
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
    # Sprite for the player Ship
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((55, 55))
        # self.image.fill(BLUE)
        self.image = player_img
        self.image = pygame.transform.scale(player_img, (55, 34))
        self.image.set_colorkey(BLACK)
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
        # check edges
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def shoot(self):
        bullet = Bullet(self.rect.centerx,  self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Mob(pygame.sprite.Sprite):
    # Sprite for the Enemy Ship
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((34, 34))
        # self.image.fill(MAGENTA)
        self.image = meteor_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-89, -55)
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(1, 2)

    def update(self):
        # update the position for the Enemy sprite
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH + 55 or self.rect.left < -55 or self.rect.bottom > HEIGHT + 55:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-89, -55)
            self.speedx = random.randrange(-3, 3)
            self.speedy = random.randrange(1, 2)


class Bullet(pygame.sprite.Sprite):
    # sprite for the bullets
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((13, 21))
        # self.image.fill(YELLOW)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -13

    def update(self):
        self.rect.y += self.speedy
        # if it goes off the screen delete the Sprite
        if self.rect.bottom < 0:
            self.kill()


# load all graphics
background = pygame.image.load(path.join(img_dir, 'starfield.png')).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, 'playerShip1_orange.png')).convert()
meteor_img = pygame.image.load(path.join(img_dir, 'meteorBrown_med1.png')).convert()
bullet_img = pygame.image.load(path.join(img_dir, 'laserRed16.png')).convert()

# Sprite Group
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
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
    # input process(events)
    for event in pygame.event.get():
        # check to see if user close the window
        if event.type == pygame.QUIT:
            running = False
        # player will shoot
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # update
    all_sprites.update()

    # check to see if any of the bullets hit the mobs
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    # check to see if any of the mobs hits the player
    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        running = False
    # draw
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    # *after* drawing everything flip the display
    pygame.display.flip()

pygame.quit()
