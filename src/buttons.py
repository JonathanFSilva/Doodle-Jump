import pygame
from pygame.locals import *

from config import *
from sprites import Sprite


class Button(Sprite):
    x = 0
    y = 0

    def __init__(self, x, y, image_on, image_off):
        self.x = x
        self.y = y

        pygame.sprite.Sprite.__init__(self)
        self.image_on = pygame.image.load(image_on)
        self.image_off = pygame.image.load(image_off)
        self.change_state(0)

    def change_state(self, state):
        if not state:
            self.image = self.image_off
        elif state:
            self.image = self.image_on

        self.image.set_colorkey(self.image.get_at((0, 0)), RLEACCEL)

        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)


class PlayButton(Button):

    def __init__(self, x, y):
        Button.__init__(self, x, y, play_button_on, play_button)


class PlayAgainButton(Button):

    def __init__(self, x, y):
        Button.__init__(self,x, y, play_again_button_on, play_again_button)