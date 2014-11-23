# /usr/bin/env python
"""
This simple example is used for the line-by-line tutorial
that comes with pygame. It is based on a 'popular' web banner.
Note there are comments here, but for the full explanation,
follow along in the tutorial.
"""


# Import Modules
import os

import pygame
from pygame.locals import *


# functions to create our resources
def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    image = image.convert()
    if color_key is not None:
        if color_key is -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key, RLEACCEL)
    return image, image.get_rect()


def load_sound(name):
    class NoneSound:
        def play(self):
            pass

    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join('data', name)
    sound = pygame.mixer.Sound(fullname)
    return sound


# classes for our game objects
class Gun(pygame.sprite.Sprite):
    """moves a clenched fist on the screen, following the mouse"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('sight.png', -1)
        self.firing = 0

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos
        if self.firing:
            self.rect.move_ip(5, 10)

    def hitontarget(self, target):
        if not self.firing:
            self.firing = 1
            hitbox = self.rect.inflate(-3, -5)
            return hitbox.colliderect(target.rect)

    def pullback(self):
        self.firing = 0


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('bird.png', -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 10
        self.move = 9
        self.move1 = 9
        self.onHit = 0

    def update(self):

        if self.onHit:
            self._spin()
        else:
            self._walk()

    def _walk(self):

        newpos = self.rect.move((self.move, self.move1))
        if self.rect.left < self.area.left or self.rect.right > self.area.right:
            self.move = -self.move
            newpos = self.rect.move((self.move, 0))
            self.image = pygame.transform.flip(self.image, 1, 0)

        if self.rect.top < self.area.top or self.rect.bottom > self.area.bottom -150:
            self.move1 = -self.move1

            newpos = self.rect.move((self.move, self.move1))
        self.rect = newpos

    def _spin(self):

        center = self.rect.center
        self.onHit += 12
        if self.onHit >= 180:
            self.onHit = 0
            self.image = self.original
        else:
            rotate = pygame.transform.rotate
            self.image = rotate(self.original, self.onHit)
        self.rect = self.image.get_rect(center=center)

    def gothit(self):

        if not self.onHit:
            self.onHit = 1
            self.original = self.image


def main():

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Duck Hunt')
    pygame.mouse.set_visible(0)

    # Background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((140, 180, 20))

    # Put Text On The Background, Centered
    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render("Duck Hunt!", 1, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width() / 2)
        background.blit(text, textpos)

    # Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Prepare Game Objects
    clock = pygame.time.Clock()
    whiff_sound = load_sound('gun.wav')
    punch_sound = load_sound('exp.wav')

    score = 0

    myfont = pygame.font.SysFont("monospace", 20)
    label1 = myfont.render("Score: " + str(score), 1, (204, 22, 0))

    bird = Bird()
    gunsight = Gun()

    allsprites = pygame.sprite.RenderPlain((gunsight, bird))

    # Main Loop
    while 1:
        clock.tick(60)
        label1 = myfont.render("Score: " + str(score), 1, (204, 22, 0))

        # Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == MOUSEBUTTONDOWN:
                if gunsight.hitontarget(bird):
                    punch_sound.play()
                    bird.gothit()
                    score += 1
                else:
                    whiff_sound.play()
            elif event.type is MOUSEBUTTONUP:
                gunsight.pullback()

        allsprites.update()


        screen.blit(background, (0, 0))
        pygame.draw.line(background, (200, 200, 200), (0, 450), (800, 450), 1)
        # Draw Everything
        screen.blit(label1, (100, 500))
        allsprites.draw(screen)
        pygame.display.flip()

# Game Over


# this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()