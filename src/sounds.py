import time
import pygame
from pygame.locals import *

from config import *


class Sound:

    def __init__(self):
        self.jump_sound = pygame.mixer.Sound(jump_sound)
        self.spring_sound = pygame.mixer.Sound(spring_sound)
        self.falling_sound = pygame.mixer.Sound(falling_sound)
        self.crashing_sound = pygame.mixer.Sound(crashing_sound)

    def play_jump_sound(self):
        self.jump_sound.set_volume(0.1)
        self.jump_sound.play()

    def play_spring_sound(self):
        self.spring_sound.set_volume(0.4)
        self.spring_sound.play()
    
    def play_falling_sound(self):
        self.falling_sound.play()
    
    def play_crashing_sound(self):
        self.crashing_sound.set_volume(0.2)
        self.crashing_sound.play()
