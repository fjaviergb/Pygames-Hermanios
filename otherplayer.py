import pygame as pg
import math
import numpy as np

###########################################################
# CLASE
###########################################################

class otherbody(pg.sprite.Sprite):
    def __init__(self, x, y, angle, anglehit, slashright, slashleft):
        super().__init__()
        self.radio = 20
        self.x = x
        self.y = y
        self.image = pg.Surface((50,50))
        pg.draw.circle(self.image, (RED), (25,25), self.radio)
        self.rect = self.image.get_rect(center = (self.x,self.y))
        self.image.set_colorkey(BLACK)    
        self.image_orig = self.image
        self.angle = angle
        self.anglehit = anglehit
        self.mask = pg.mask.from_surface(self.image) 
        self.slashright = slashright
        self.slashleft = slashleft        
        
    def update(self, player):
        self.image = pg.transform.rotate(self.image_orig, self.angle)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.mask = pg.mask.from_surface(self.image)                  
        
    class otherRhand(pg.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.radio = 10
            self.image = pg.Surface((50,50))
            self.image.set_colorkey(BLACK)
            pg.draw.circle(self.image, (GREEN), (40,10), self.radio)
            self.rect = self.image.get_rect(center = (150,150))
            self.image_orig = self.image
            self.mask = pg.mask.from_surface(self.image)                  
            
        def update(self, player):
            self.image = pg.transform.rotate(self.image_orig, player.anglehit)
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect(center = player.rect.center)
            self.mask = pg.mask.from_surface(self.image)                  
    
    class otherLhand(pg.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.radio = 10
            self.image = pg.Surface((50,50))
            self.image.set_colorkey(BLACK)            
            pg.draw.circle(self.image, (BLUE), (10,10), self.radio)
            self.rect = self.image.get_rect(center = (150,150))
            self.image_orig = self.image            
            self.mask = pg.mask.from_surface(self.image)                  
            
        def update(self, player):
            self.image = pg.transform.rotate(self.image_orig, player.angle)
            self.image.set_colorkey(BLACK)            
            self.rect = self.image.get_rect(center = player.rect.center)
            self.mask = pg.mask.from_surface(self.image)                  
    
    class othersword(pg.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pg.Surface((50,120))
            pg.draw.rect(self.image, RED, (40,0,5,50))
            self.rect = self.image.get_rect(center = (150,150))
            self.image.set_colorkey(BLACK)        
            self.image_orig = self.image
            self.mask = pg.mask.from_surface(self.image)                  

        def update(self, player):
            self.image = pg.transform.rotate(self.image_orig, player.anglehit)
            self.image.set_colorkey(BLACK)            
            self.rect = self.image.get_rect(center = player.rect.center)
            self.mask = pg.mask.from_surface(self.image)                  

            
CBASE = (255,255,255)
CPLAYER = (255,228,181)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
GOLD = (255,215,0)
WHITE = (255,255,255)
