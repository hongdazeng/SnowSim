# /usr/bin/env python
"""
Purdue Computer Science Women's Network / Microsoft Hackathon Project
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
        self.move = 8
        self.move1 = 9
        self.onHit = 0

    def update(self):

        if self.onHit:
            self._spin()
        else:
            self._walk()

    def _walk(self):

        new_pos = self.rect.move((self.move, self.move1))
        if self.rect.left < self.area.left or self.rect.right > self.area.right:
            self.move = -self.move
            new_pos = self.rect.move((self.move, 0))
            self.image = pygame.transform.flip(self.image, 1, 0)

        if self.rect.top < self.area.top or self.rect.bottom > self.area.bottom - 150:
            self.move1 = -self.move1

            new_pos = self.rect.move((self.move, self.move1))
        self.rect = new_pos

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
            # noinspection PyAttributeOutsideInit
            self.original = self.image

    def movefaster(self):

        move_point = 4

        if self.move > 0:
            self.move += move_point
        elif self.move < 0:
            self.move -= move_point

        if self.move1 > 0:
            self.move1 += move_point
        elif self.move1 < 0:
            self.move -= move_point

    def completestop(self):
        self.move = 0
        self.move1 = 0


def main():

    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
    pygame.display.set_caption('Duck Hunt')
    pygame.mouse.set_visible(0)

    # Background
    # noinspection PyArgumentList
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
    miss_sound = load_sound('gun.wav')
    hit_sound = load_sound('exp.wav')
    level_sound = load_sound('tone.wav')
    sound_name = os.path.join('data', 'star.ogg')
    pygame.mixer.music.load(sound_name)
    pygame.mixer.music.play(0)

    score = 0
    s_level = 0
    level = 0
    rounds = 10

    myfont = pygame.font.SysFont("monospace", 20)

    bird = Bird()
    gunsight = Gun()

    allsprites = pygame.sprite.RenderPlain((gunsight, bird))
    label_name = myfont.render("Created by Hongda Zeng", 1, (204, 22, 0))

    # Main Loop
    while 1:
        clock.tick(50)
        label1 = myfont.render("Score: " + str(score), 1, (204, 22, 0))
        label2 = myfont.render("Level: " + str(level) + " Spd" + str(abs(bird.move)), 1, (204, 22, 0))

        # Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == MOUSEBUTTONDOWN:

                rounds -= 1

                if gunsight.hitontarget(bird):
                    hit_sound.play()
                    bird.gothit()
                    score += 1
                    s_level += 0.2

                    if s_level > 0.9:
                        bird.movefaster()
                        level_sound.play()
                        rounds = 10
                        s_level = 0
                        level += 1

                else:
                    miss_sound.play()

            if rounds <= 0:
                    bird.completestop()
                    label4 = myfont.render("-=Game Over=- Press any key to quit", 1, (204, 22, 0))
                    pygame.mixer.music.pause()
                    a = True
                    while a:
                        screen.blit(label1, (100, 500))
                        screen.blit(label2, (120, 550))
                        # noinspection PyUnboundLocalVariable
                        screen.blit(label3, (400, 500))
                        screen.blit(label4, (200, 300))
                        screen.blit(label_name, (420, 550))
                        allsprites.draw(screen)
                        pygame.display.flip()
                        # noinspection PyAssignmentToLoopOrWithParameter
                        for event in pygame.event.get():  # User did something
                            if event.type == pygame.QUIT:  # If user clicked close
                                return
                            elif event.type == pygame.KEYDOWN:
                                return

            elif event.type is MOUSEBUTTONUP:
                gunsight.pullback()
        label3 = myfont.render("Bullets: " + str(rounds), 1, (204, 22, 0))
        allsprites.update()

        screen.blit(background, (0, 0))
        pygame.draw.line(background, (200, 200, 200), (0, 450), (800, 450), 1)
        # Draw Everything
        screen.blit(label1, (100, 500))
        screen.blit(label2, (120, 550))
        screen.blit(label3, (400, 500))
        screen.blit(label_name, (420, 550))
        allsprites.draw(screen)
        pygame.display.flip()

# Game Over


# this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()