import pygame as pg

##################################################################
# CLASE OBSTÁCULO RECTANGULAR
##################################################################
class rect_obstacle(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.Surface((700,700))
        pg.draw.rect(self.image, BROWN, (0, 0, 700, 700))
        pg.draw.rect(self.image, BLACK, (5, 5, 690, 690))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pg.mask.from_surface(self.image)
        self.tipo = 3
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
BROWN = (108,95,55)