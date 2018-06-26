import pygame
from pygame.locals import *

from sprites import Sprite

from config import *


class Doodle(Sprite):

    name = 'Anonymus'
    score = 0

    alive = True
    ySpeed = 5

    x = doodle_start_position[0]
    y = doodle_start_position[1]

    def __init__(self, name='Anonymus'):
        pygame.sprite.Sprite.__init__(self)

        self.name = name

        self.image_left = pygame.image.load(doodle)
        self.image_right = pygame.transform.flip(self.image_left, True, False)

        self.image = self.image_right
        self.image.set_colorkey(self.image.get_at((0, 0)), RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def _move(self):
        self.rect.center = (self.x, self.y)
        if self.y >= screen_height:
            self.alive = False

    def get_legs_rect(self):
        left = self.rect.left + self.rect.width * 0.1
        top = self.rect.top + self.rect.height * 0.9
        width = self.rect.width * 0.6
        height = self.rect.height * 0.1
        return pygame.Rect(left, top, width, height)

    def set_x(self, x):

        if x < self.x:
            self.image = self.image_left
        elif x > self.x:
            self.image = self.image_right

        self.x = x
        self.image.set_colorkey(self.image.get_at((0, 0)), RLEACCEL)
        self.rect = self.image.get_rect()
        self._move()

    def inc_y_speed(self, speed):
        self.ySpeed += speed

    def inc_score(self, score):
        self.score += score