#!/usr/bin/env python3
import sys

import pygame
from pygame.locals import *

from locations import GameLocation, StartLocation

from config import *


class Game(object):

    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()

        pygame.display.set_caption('Doodle Jump')
        window = pygame.display.set_mode(screen_size)

    def event(self, event):
        if event.type == QUIT:
            sys.exit()
        elif event.type == KEYUP:
            if event.key == K_ESCAPE:
                if isinstance(self.location, GameLocation):
                    self.location = StartLocation(self)
                elif isinstance(self.location, StartLocation):
                    sys.exit()


if __name__ == "__main__":
    game = Game()

    start_location = StartLocation(game)

    # game.location = GameLocation(game)
    game.location = start_location

    clock = pygame.time.Clock()
    while True:
        clock.tick(fps)
        
        game.location.draw()
        pygame.display.flip()

        for event in pygame.event.get():
            game.location.event(event)
            game.event(event)
