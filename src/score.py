import pygame
from pygame.locals import *

from sprites import Sprite


class Score(Sprite):

    def __init__(self, x, y, text='', size=35, color=(255, 255, 255)):
        pygame.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y

        self.font = pygame.font.Font(None, size)
        self.color = color
        self.text = text

        self.generate_image()

    def set_text(self, text):
        self.text = text
        self.generate_image()

    def set_color(self, color):
        self.generate_image()

    def set_size(self, size):
        self.font = pygame.Font(None, size)
        self.generate_image()

    def generate_image(self):
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)