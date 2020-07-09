import pygame as pg
import math
import numpy as np

###########################################################
# CLASE
###########################################################

class body(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.radio = 20
        self.x = 150
        self.y = 150
        self.image = pg.Surface((50,50))
        pg.draw.circle(self.image, (RED), (25,25), self.radio)
        self.rect = self.image.get_rect(center = (self.x,self.y))
        self.vel = 3
        self.image.set_colorkey(BLACK)                
        self.image_orig = self.image
        self.movex = 0
        self.movey = 0
        self.angle = 0
        self.anglehit = 0
        self.swingleft = False
        self.swingright = False
        self.slashright = False
        self.slashleft = False
        self.backleft = False
        self.backright = False
        self.hitorient = 2
        self.hittin = False
        self.chargecount = 1
        self.countlimit = 0
        
    def update(self, player):
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            self.x -= self.vel
        if keys[pg.K_RIGHT]:
            self.x += self.vel
        if keys[pg.K_UP]:
            self.y -= self.vel
        if keys[pg.K_DOWN]:
            self.y += self.vel

        button = pg.mouse.get_pressed()
        (xcursor, ycursor) = pg.mouse.get_pos()
        sen = ycursor - player.rect.centery
        cos = xcursor - player.rect.centerx

######################################################################
# ROTACIÓN + COMIENZO ESPADAZO 
######################################################################
        ######################################################################
        # HITO PARA EVITAR DIVISION ENTRE INFINITO
        ######################################################################
        if cos != 0:
            angle_rad = math.atan(sen / cos)
            angle_grad = angle_rad * 360 / (2 * math.pi)            
        ######################################################################
        # CUADRANTE DERECHA
        ######################################################################
            if cos > 0:
                self.angle = 270 - angle_grad    
                if button[2] != 0 and not self.swingleft and not self.swingright and not self.slashleft and not self.slashright and not self.backleft and not self.backright:
                    self.hitorient = 1                                        
                    self.swingright = True
                    self.anglehit = 270 - angle_grad - 90
                elif button[0] != 0 and not self.swingleft and not self.swingright and not self.slashleft and not self.slashright and not self.backleft and not self.backright:
                    self.hitorient = 0           
                    self.swingleft = True
                    self.anglehit = 270 - angle_grad + 90
                elif button[2] == 0 and button[0] == 0 and not self.swingleft and not self.swingright and not self.slashleft and not self.slashright and not self.backleft and not self.backright:
                    self.anglehit = 270 - angle_grad
                    
                ###########################################################              
                # ESPADAZO DESDE LA DERECHA
                ###########################################################
                if self.swingright:
                    if self.chargecount <= 30:
                        self.anglehit = 270 - angle_grad - self.chargecount * 90 / 30
                        self.chargecount += 1
                    elif button[2] == 0:
                        self.countlimit = self.chargecount                        
                        self.slashright = True
                        self.swingright = False                        
                elif self.slashright and not self.swingright and not self.backright:
                    if self.chargecount >= self.countlimit * -20 / 30:
                            self.anglehit = 270 - angle_grad - self.chargecount * 90 / 30
                            self.chargecount -= 1
                    else:
                        self.slashright = False                
                        self.backright = True
                elif self.backright:
                    if self.chargecount <= 1:
                        self.anglehit = 270 - angle_grad - self.chargecount * 90 / 30
                        self.chargecount += 1    
                    else:                 
                        self.backright = False
                        self.chargecount = 1
                    
                ###########################################################              
                # ESPADAZO DESDE LA IZQUIERDA
                ###########################################################
                if self.swingleft:
                    if self.chargecount <= 30:
                        self.anglehit = 270 - angle_grad + self.chargecount * 90 / 30
                        self.chargecount += 1
                    elif button[0] == 0:
                        self.countlimit = self.chargecount
                        self.slashleft = True
                        self.swingleft = False                        
                elif self.slashleft and not self.swingleft and not self.backleft:
                    if self.chargecount >= self.countlimit * -20 / 30:
                            self.anglehit = 270 - angle_grad + self.chargecount * 90 / 30
                            self.chargecount -=  1                
                    else:
                        self.slashleft = False                
                        self.backleft = True
                elif self.backleft:
                    if self.chargecount <= 1:
                        self.anglehit = 270 - angle_grad + self.chargecount * 90 / 30
                        self.chargecount += 1    
                    else:                 
                        self.backleft = False
                        self.chargecount = 1
                
        ######################################################################
        # CUADRANTE IZQUIERDA
        ######################################################################
            elif cos < 0:
                self.angle = 90 - angle_grad
                if button[2] != 0 and not self.swingleft and not self.swingright and not self.slashleft and not self.slashright and not self.backleft and not self.backright:
                    self.hitorient = 1                                        
                    self.swingright = True
                    self.anglehit = 90 - angle_grad - 90
                elif button[0] != 0 and not self.swingleft and not self.swingright and not self.slashleft and not self.slashright and not self.backleft and not self.backright:
                    self.hitorient = 0           
                    self.swingleft = True
                    self.anglehit = 90 - angle_grad + 90
                elif button[2] == 0 and button[0] == 0 and not self.swingleft and not self.swingright and not self.slashleft and not self.slashright and not self.backleft and not self.backright:
                    self.anglehit = 90 - angle_grad

                ###########################################################              
                # ESPADAZO DESDE LA DERECHA
                ###########################################################
                if self.swingright:
                    if self.chargecount <= 30:
                        self.anglehit = 90 - angle_grad - self.chargecount * 90 / 30
                        self.chargecount += 1
                    elif button[2] == 0:
                        self.countlimit = self.chargecount                        
                        self.slashright = True
                        self.swingright = False                        
                elif self.slashright and not self.swingright and not self.backright:
                    if self.chargecount >= self.countlimit * -20 / 30:
                            self.anglehit = 90 - angle_grad - self.chargecount * 90 / 30
                            self.chargecount -= 1
                    else:
                        self.slashright = False                
                        self.backright = True
                elif self.backright:
                    if self.chargecount <= 1:
                        self.anglehit = 90 - angle_grad - self.chargecount * 90 / 30
                        self.chargecount += 1    
                    else:                 
                        self.backright = False
                        self.chargecount = 1
                    
                ###########################################################              
                # ESPADAZO DESDE LA IZQUIERDA
                ###########################################################
                if self.swingleft:
                    if self.chargecount <= 30:
                        self.anglehit = 90 - angle_grad + self.chargecount * 90 / 30
                        self.chargecount += 1
                    elif button[0] == 0:
                        self.countlimit = self.chargecount                        
                        self.slashleft = True
                        self.swingleft = False                        
                elif self.slashleft and not self.swingleft and not self.backleft:
                    if self.chargecount >= self.countlimit * -20 / 30:
                            self.anglehit = 90 - angle_grad + self.chargecount * 90 / 30
                            self.chargecount -=  1               
                    else:
                        self.slashleft = False                
                        self.backleft = True
                elif self.backleft:
                    if self.chargecount <= 1:
                        self.anglehit = 90 - angle_grad + self.chargecount * 90 / 30
                        self.chargecount += 1    
                    else:                 
                        self.backleft = False
                        self.chargecount = 1
                
        ######################################################################
        # HITO CON DIVISION INFINITO, CUADRANTE SUPERIOR
        ######################################################################
        elif cos == 0 and sen < 0:
            self.angle = 0
            if button[2] != 0 and not self.swingleft and not self.swingright and not self.slashleft and not self.slashright and not self.backleft and not self.backright:
                self.hitorient = 1                                        
                self.swingright = True
            elif button[0] != 0 and not self.swingleft and not self.swingright and not self.slashleft and not self.slashright and not self.backleft and not self.backright:
                self.hitorient = 0           
                self.swingleft = True

            ###########################################################              
            # ESPADAZO DESDE LA DERECHA
            ###########################################################
            if self.swingright:
                if self.chargecount <= 30:
                    self.anglehit = 0 - self.chargecount * 90 / 30
                    self.chargecount += 1
                elif button[2] == 0:
                    self.countlimit = self.chargecount                    
                    self.slashright = True
                    self.swingright = False                        
            elif self.slashright and not self.swingright and not self.backright:
                if self.chargecount >= self.countlimit * -20 / 30:
                        self.anglehit = 0 - self.chargecount * 90 / 30
                        self.chargecount -= 1
                else:
                    self.slashright = False                
                    self.backright = True
            elif self.backright:
                if self.chargecount <= 1:
                    self.anglehit = 0 - self.chargecount * 90 / 30
                    self.chargecount += 1    
                else:                 
                    self.backright = False
                    self.chargecount = 1
                
            ###########################################################              
            # ESPADAZO DESDE LA IZQUIERDA
            ###########################################################
            if self.swingleft:
                if self.chargecount <= 30:
                    self.anglehit = 0 + self.chargecount * 90 / 30
                    self.chargecount += 1
                elif button[0] == 0:
                    self.countlimit = self.chargecount                                        
                    self.slashleft = True
                    self.swingleft = False                        
            elif self.slashleft and not self.swingleft and not self.backleft:
                if self.chargecount >= self.countlimit * -20 / 30:
                        self.anglehit = 0 + self.chargecount * 90 / 30
                        self.chargecount -=  1                
                else:
                    self.slashleft = False                
                    self.backleft = True
            elif self.backleft:
                if self.chargecount <= 1:
                    self.anglehit = 0 + self.chargecount * 90 / 30
                    self.chargecount += 1    
                else:                 
                    self.backleft = False
                    self.chargecount = 1
            
        ######################################################################
        # HITO CON DIVISION INFINITO, CUADRANTE INFERIOR
        ######################################################################
        elif cos == 0 and sen > 0:
            self.angle = 180
            if button[2] != 0 and not self.swingleft and not self.swingright and not self.slashleft and not self.slashright and not self.backleft and not self.backright:
                self.hitorient = 1                                        
                self.swingright = True
            elif button[0] != 0 and not self.swingleft and not self.swingright and not self.slashleft and not self.slashright and not self.backleft and not self.backright:
                self.hitorient = 0           
                self.swingleft = True

            ###########################################################              
            # ESPADAZO DESDE LA DERECHA
            ###########################################################
            if self.swingright:
                if self.chargecount <= 30:
                    self.anglehit = 180 - self.chargecount * 90 / 30
                    self.chargecount += 1
                elif button[2] == 0:
                    self.countlimit = self.chargecount                                                         
                    self.slashright = True
                    self.swingright = False                        
            elif self.slashright and not self.swingright and not self.backright:
                if self.chargecount >= self.countlimit * -20 / 30:
                        self.anglehit = 180 - self.chargecount * 90 / 30
                        self.chargecount -= 1
                else:
                    self.slashright = False                
                    self.backright = True
            elif self.backright:
                if self.chargecount <= 1:
                    self.anglehit = 180 - self.chargecount * 90 / 30
                    self.chargecount += 1    
                else:                 
                    self.backright = False
                    self.chargecount = 1
                
            ###########################################################              
            # ESPADAZO DESDE LA IZQUIERDA
            ###########################################################
            if self.swingleft:
                if self.chargecount <= 30:
                    self.anglehit = 180 + self.chargecount * 90 / 30
                    self.chargecount += 1
                elif button[0] == 0:
                    self.countlimit = self.chargecount                    
                    self.slashleft = True
                    self.swingleft = False                        
            elif self.slashleft and not self.swingleft and not self.backleft:
                if self.chargecount >= self.countlimit * -20 / 30:
                        self.anglehit = 180 + self.chargecount * 90 / 30
                        self.chargecount -=  8                
                else:
                    self.slashleft = False                
                    self.backleft = True
            elif self.backleft:
                if self.chargecount <= 1:
                    self.anglehit = 180 + self.chargecount * 90 / 30
                    self.chargecount += 1    
                else:                 
                    self.backleft = False
                    self.chargecount = 1

        print(button, self.chargecount, self.swingright, self.slashright, self.backright)
#        print(button, self.chargecount, self.swingleft, self.slashleft, self.backleft)
        
        self.image = pg.transform.rotate(self.image_orig, self.angle)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center = (self.x, self.y))
 
        
    class Rhand(pg.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.radio = 10
            self.handspeed = 1
            self.hitcount = 10
            self.image = pg.Surface((50,50))
            self.image.set_colorkey(BLACK)
            pg.draw.circle(self.image, (GREEN), (40,10), self.radio)
            self.rect = self.image.get_rect(center = (150,150))
            self.image_orig = self.image
            
        def update(self, player):
            self.image = pg.transform.rotate(self.image_orig, player.anglehit)
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect(center = player.rect.center)
    
    class Lhand(pg.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.radio = 10
            self.handspeed = 1
            self.hitcount = 10
            self.image = pg.Surface((50,50))
            self.image.set_colorkey(BLACK)            
            pg.draw.circle(self.image, (BLUE), (10,10), self.radio)
            self.rect = self.image.get_rect(center = (150,150))
            self.image_orig = self.image            
            
            
        def update(self, player):
            self.image = pg.transform.rotate(self.image_orig, player.angle)
            self.image.set_colorkey(BLACK)            
            self.rect = self.image.get_rect(center = player.rect.center)
    
    class sword(pg.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pg.Surface((50,120))
            pg.draw.rect(self.image, RED, (40,0,5,50))
            self.rect = self.image.get_rect(center = (150,150))
            self.image.set_colorkey(BLACK)        
            self.image_orig = self.image

        def update(self, player):
            self.image = pg.transform.rotate(self.image_orig, player.anglehit)
            self.image.set_colorkey(BLACK)            
            self.rect = self.image.get_rect(center = player.rect.center)

            
CBASE = (255,255,255)
CPLAYER = (255,228,181)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
GOLD = (255,215,0)
WHITE = (255,255,255)
       