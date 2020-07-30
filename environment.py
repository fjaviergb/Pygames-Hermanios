import pygame as pg
import math
import numpy as np

##################################################################
# CLASE OBSTÁCULO
##################################################################
class gir_obstacle(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.live = 6
        self.image = pg.Surface((50, 150))
        pg.draw.rect(self.image, BLUE, (20, 25, 10, 100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pg.mask.from_surface(self.image)
        self.image_orig = self.image
        self.counter = 0
        self.crash = False
        self.tipo = 2
        self.x = x
        self.y = y

    def update(self):
        if not self.crash:
            if self.counter <= 360:
                self.image = pg.transform.rotate(self.image_orig, 6 * self.counter)
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect(center=self.rect.center)
                self.mask = pg.mask.from_surface(self.image)
                self.counter += 1
            else:
                self.counter = 0
        else:
            pass


##################################################################
# CLASE OBSTÁCULO RECTANGULAR
##################################################################
class rect_obstacle(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.Surface((100, 50))
        pg.draw.rect(self.image, BLUE, (5, 5, 90, 40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pg.mask.from_surface(self.image)
        self.live = 3
        self.counter = 0
        self.tipo = 3
        self.x = x
        self.y = y


##################################################################
# CLASE OBSTÁCULO CIRCULAR
##################################################################
class circle_obstacle(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.Surface((150, 150))
        pg.draw.circle(self.image, BLUE, (75, 75), 75)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pg.mask.from_surface(self.image)
        self.live = 3
        self.counter = 0
        self.tipo = 4
        self.x = x
        self.y = y


CBASE = (255, 255, 255)
CPLAYER = (255, 228, 181)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)
WHITE = (255, 255, 255)
