import sys
import random
import pygame
from pygame.locals import *

from config import *
from score import Score
from doodle import Doodle
from sounds import Sound
from buttons import PlayButton, PlayAgainButton
from platform import Spring, Platform, MovingPlatform, CrashingPlatform



class Location(object):
    parent = None

    def __init__(self, parent, background):
        self.window = pygame.display.get_surface()
        self.parent = parent
        self.background = pygame.image.load(background)
        self.background = pygame.transform.scale(self.background, (480, 640))

    def event(self, event):
        pass

    def draw(self):
        pass


class StartLocation(Location):

    def __init__(self, parent):
        Location.__init__(self, parent, menu_background)
        
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(-1)
        
        pygame.mouse.set_visible(1)
        pygame.key.set_repeat(0)


        self.start_button = PlayButton(240, 300)

        self.surfaces = []
        self.controls = pygame.sprite.Group()
        self.controls.add(self.start_button)
        
        self.platform1 = Platform(120, 600)
        self.platform2 = Platform(240, 490)
        self.platform3 = Platform(360, 550)
        self.doodle = Doodle()

        self.animation = pygame.sprite.Group()
        self.animation.add(self.platform1)
        self.animation.add(self.platform2)
        self.animation.add(self.platform3)
        self.animation.add(self.doodle)

        self.window.blit(self.background, (0, 0))

    def draw(self):
        self.controls.clear(self.window, self.background)
        self.animation.clear(self.window, self.background)

        self.doodle.set_x(125)
        self.doodle.inc_y_speed(-gravitation)
        self.doodle.move_y(-self.doodle.ySpeed)

        if self.doodle.get_legs_rect().top >= 590:
            self.doodle.ySpeed = 10

        self.controls.draw(self.window)
        self.animation.draw(self.window)


    def event(self, event):
        if event.type == MOUSEMOTION:
            for btn in self.controls:
                if btn.rect.collidepoint(pygame.mouse.get_pos()):
                    btn.change_state(1)
                else:
                    btn.change_state(0)
        elif event.type == MOUSEBUTTONUP:
            if self.start_button.rect.collidepoint(pygame.mouse.get_pos()):
                self.parent.location = GameLocation(self.parent, 'Anonymous')

class EndLocation(Location):

    def __init__(self, parent, score):
        Location.__init__(self, parent, end_background)

        self.save_score(score)

        pygame.mouse.set_visible(1)
        pygame.key.set_repeat(0)

        self.start_button = PlayAgainButton(240, 250)
        
        self.message1 = Score(240, 350, "Your score: ", 50, (0, 0, 0))
        self.score = Score(240, 400, str(score), 45, (0, 0, 0))

        self.message2 = Score(240, 450, "Your high score: ", 50, (0, 0, 0))
        self.high_score = Score(240, 500, str(self.get_high_score()), 45, (0, 0, 0))

        self.surfaces = []
        self.controls = pygame.sprite.Group()
        self.controls.add(self.start_button)
        
        self.messages = pygame.sprite.Group()
        self.messages.add(self.message1)
        self.messages.add(self.message2)
        self.messages.add(self.score)
        self.messages.add(self.high_score)
        
        self.window.blit(self.background, (0, 0))

    def draw(self):
        self.controls.clear(self.window, self.background)
        self.controls.draw(self.window)
        self.messages.draw(self.window)


    def event(self, event):
        if event.type == MOUSEMOTION:
            for btn in self.controls:
                if btn.rect.collidepoint(pygame.mouse.get_pos()):
                    btn.change_state(1)
                else:
                    btn.change_state(0)
        elif event.type == MOUSEBUTTONUP:
            if self.start_button.rect.collidepoint(pygame.mouse.get_pos()):
                self.parent.location = GameLocation(self.parent, 'Anonymous')

    def get_high_score(self):
        with open('.scores.txt', 'r') as base:
            scores = []
            for score in base.readlines():
                scores.append(int(score.strip()))

        high_score = max(scores)  
        return high_score    

    def save_score(self, score):
        with open('.scores.txt', 'a') as base:
            base.write(str(score)+'\n')


class GameLocation(Location):

    def __init__(self, parent, name='Anonymus'):
        Location.__init__(self, parent, background)
        pygame.key.set_repeat(10)
        pygame.mouse.set_visible(mouse_enabled)

        self.sound = Sound()

        self.doodle = Doodle(name)
        self.allsprites = pygame.sprite.Group()
        self.allsprites.add(self.doodle)

        for i in range(0, platform_count):
            self.allsprites.add(self.randomPlatform(False))
        for platform in self.allsprites:
            if isinstance(platform, Platform) and platform.spring != None:
                self.allsprites.add(platform.spring)

        self.score = Score(50, 25, self.doodle.name, 45, (0, 0, 0))
        self.allsprites.add(self.score)
        self.window.blit(self.background, (0, 0))

    def randomPlatform(self, top=True):
        x = random.randint(0, screen_width - platform_width)
        bad_y = []

        for spr in self.allsprites:
            bad_y.append((spr.y - platform_y_padding, spr.y + platform_y_padding + spr.rect.height))
    
        good = 0
        while not good:
            if top:
                y = random.randint(-100, 100)
            else:
                y = random.randint(0, screen_height)

            good = 1
            for bad_y_item in bad_y:
                if bad_y_item[0] <= y <= bad_y_item[1]:
                    good = 0
                    break

        dig = random.randint(0, 100)
        if dig < 35:
            return MovingPlatform(x, y)
        elif 35 <= dig < 50:
            return CrashingPlatform(x, y) 
        else:
            return Platform(x, y)

    def draw(self):
        if self.doodle.alive:

            self.allsprites.clear(self.window, self.background)

            mousePos = pygame.mouse.get_pos()
            self.doodle.inc_y_speed(-gravitation)
            if mouse_enabled:
                self.doodle.set_x(mousePos[0])
            else:
                if transparent_walls:
                    if self.doodle.x < 0:
                        self.doodle.set_x(screen_width)
                    elif self.doodle.x > screen_width:
                        self.doodle.set_x(0)

            self.doodle.move_y(-self.doodle.ySpeed)

            for spr in self.allsprites:
                if isinstance(spr, Spring) and self.doodle.get_legs_rect().colliderect(spr.get_top_surface()) and self.doodle.ySpeed <= 0:
                    self.sound.play_spring_sound()
                    spr.compress()
                    self.doodle.ySpeed = spring_speed
                    

                if isinstance(spr, Platform) and self.doodle.get_legs_rect().colliderect(spr.get_surface_rect()) and self.doodle.ySpeed <= 0:
                    if isinstance(spr, CrashingPlatform):
                        if not spr.is_playing:
                            spr.is_playing = True
                            self.sound.play_crashing_sound()
                        spr.crash()
                        break

                    self.sound.play_jump_sound()
                    self.doodle.ySpeed = jump_speed

                if isinstance(spr, Platform):
                    if spr.y >= screen_height:
                        self.allsprites.remove(spr)
                        platform = self.randomPlatform()
                        self.allsprites.add(platform)
                        if isinstance(platform, Platform) and platform.spring != None:
                            self.allsprites.add(platform.spring)

                if isinstance(spr,MovingPlatform) or (isinstance(spr,CrashingPlatform) and spr.crashed == 1):
                    spr.move()

            if self.doodle.y < horizont:
                self.doodle.inc_score(self.doodle.ySpeed)
                for spr in self.allsprites:
                    if not isinstance(spr, Score):
                        spr.move_y(self.doodle.ySpeed)

            self.allsprites.draw(self.window)
            self.score.set_text("   %s" % (int(self.doodle.score/10)))
            # self.window.blit()
        else:
            self.sound.play_falling_sound()
            # self.parent.location = GameLocation(self.parent, self.doodle.name)
            # self.parent.location = StartLocation(self.parent)
            self.parent.location = EndLocation(self.parent, int(self.doodle.score/10))

    def event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                self.doodle.set_x(self.doodle.x - 10)
            elif event.key == K_RIGHT:
                self.doodle.set_x(self.doodle.x + 10)

class ExitLocation(Location):

    def __init__(self, parent, name, score):
        Location.__init__(self, parent)
        self.background = pygame.image.load(background)
        print("Exiting")
