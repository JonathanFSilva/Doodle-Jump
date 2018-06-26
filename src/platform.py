import random
import pygame
from pygame.locals import *

from config import *
from sprites import Sprite


class Spring(Sprite):

    def __init__(self, x, y):
        self.x = x
        self.y = y

        compressed = False

        pygame.sprite.Sprite.__init__(self)

        self.init_image(spring)

    def compress(self):
        self.init_image(spring_compressed)
        self.compressed = True

    def get_top_surface(self):
        left = self.rect.left
        top = self.rect.top
        width = self.rect.width
        height = self.rect.height

        return pygame.Rect(left, top, width, height)


class Platform(Sprite):

    def __init__(self, x, y):
        Sprite.__init__(self, x, y)
        if type(self).__name__ == "Platform":
            self.init_image(fixed_platform)
            rnd = random.randint(-100, 100)
            if rnd >= 50:
                self.spring = Spring(self.x + random.randint(-int(platform_width/2 - 10), int(platform_width/2) - 10), self.y-10)
            else:
                self.spring = None

    def get_surface_rect(self):
        left = self.rect.left
        top = self.rect.top
        width = self.rect.width
        height = self.rect.height*0.1

        return pygame.Rect(left, top, width, height)


class MovingPlatform(Platform):

    def __init__(self, x, y):
        Platform.__init__(self, x, y)

        self.init_image(moving_platform)
        self.way = -1
        self.xSpeed = random.randint(2, 6)
        self.spring = None

    def move(self):
        self.move_x(self.xSpeed * self.way)

        if 10 < self.x < 19 or 460 < self.x < 469:
            self.way = -self.way


class CrashingPlatform(Platform):

    def __init__(self, x, y):
        Platform.__init__(self, x, y)

        self.init_image(crashing_platform)
        self.ySpeed = 10
        self.crashed = False
        self.spring = None
        self.img = 0
        self.is_playing = False

    def crash(self):
        # self.init_image(imgs[self.img-1])
        self.crashed = True

    def move(self):
        imgs = [crashing_platform1, crashing_platform2, crashing_platform3]
        if not self.crashed:
            pass
        elif self.crashed:
            if self.img < 3:
                self.init_image(imgs[self.img])
                self.img += 1
            self.move_y(self.ySpeed)

    def renew(self):
        Platform.renew(self)
        self.init_image(crashing_platform)
        self.crashed = False
        self.img = 0
