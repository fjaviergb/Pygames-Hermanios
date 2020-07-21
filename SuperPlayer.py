import pygame as pg
import math
import numpy as np
from otherplayer import otherbody

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
        self.mask = pg.mask.from_surface(self.image)                  
        self.vel = 2
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
        self.clashright = False
        self.clashleft = False
        self.hitorient = 2
        self.hittin = False
        self.chargecount = 1
        self.countlimit = 0
        self.clash_count = 0
        self.other_sprites = pg.sprite.Group()
        self.col_sprites = pg.sprite.Group()
        self.enem_sword = pg.sprite.Group()        
        self.live = 5
        self.rightH = self.Rhand()
        self.leftH = self.Lhand()
        self.espada = self.sword()
        self.tipo = 1
        self.env_sprites = pg.sprite.Group()
        self.blocking = False

    ###########################################################
    # FUNCION COLISION ESPADA
    ###########################################################
    def isClash(self, angle_grad, signo, angle):
        #  Metodo para depurar la colision en movimiento.
        #  Como dos objetos en "movimiento" pueden superponerse sin llegar a colisionar
        #  hacemos un pequenno barrido de los angulos para ver si se encuentran.
        for i in np.arange(0, 4, 0.5):
            #  TODO si el objeto es pequenno puede fallar.
            self.anglehit = angle - angle_grad + signo * (self.chargecount - i) * 3
            self.espada.image = pg.transform.rotate(self.espada.image_orig, self.anglehit)
            self.espada.rect = self.espada.image.get_rect(center = self.rect.center)
            self.espada.mask = pg.mask.from_surface(self.espada.image)                  
            if self.espada.image != self.espada.image_orig and ((self.slashleft and not self.swingleft and not self.backleft) or (self.slashright and not self.swingright and not self.backright)):
                block_hit_list = pg.sprite.spritecollide(self.espada, self.col_sprites, False)         
                block_hit_list_masked = pg.sprite.spritecollide(self.espada, block_hit_list, False, pg.sprite.collide_mask)        
                if len(block_hit_list_masked) == 0:
                    pass
                else:
                    break
            else:
                pass
        return i

    ###########################################################
    # FUNCION COLISION CUERPO
    ###########################################################
    def isBlockX(self, signo):
        #  Metodo para depurar la colision en movimiento.
        #  Como dos objetos en "movimiento" pueden superponerse sin llegar a colisionar
        #  hacemos un pequenno barrido de los angulos para ver si se encuentran.
        for i in np.arange(0, self.vel, 0.5):
            #  TODO si el objeto es pequenno puede fallar.
            self.x += i * signo
            self.rect = self.image.get_rect(center = (self.x, self.y))
            self.mask = pg.mask.from_surface(self.image)            
            
            block_hit_list = pg.sprite.spritecollide(self, self.col_sprites, False)         
            block_hit_list_masked = pg.sprite.spritecollide(self, block_hit_list, False, pg.sprite.collide_mask)        
            if len(block_hit_list_masked) == 0:
                pass
            else:
                return (i-0.5) * signo
                break
        return i * signo

    ###########################################################
    # FUNCION COLISION CUERPO
    ###########################################################
    def isBlockY(self, signo):
        #  Metodo para depurar la colision en movimiento.
        #  Como dos objetos en "movimiento" pueden superponerse sin llegar a colisionar
        #  hacemos un pequenno barrido de los angulos para ver si se encuentran.
        for i in np.arange(0, self.vel, 0.5):
            #  TODO si el objeto es pequenno puede fallar.
            self.y += i * signo
            self.rect = self.image.get_rect(center = (self.x, self.y))
            self.mask = pg.mask.from_surface(self.image)            
            
            block_hit_list = pg.sprite.spritecollide(self, self.col_sprites, False)         
            block_hit_list_masked = pg.sprite.spritecollide(self, block_hit_list, False, pg.sprite.collide_mask)        
            if len(block_hit_list_masked) == 0:
                pass
            else:
                return (i-0.5) * signo
                break
        return i * signo

    ###########################################################
    # FUNCION COLISION EN PARADO
    ###########################################################
    def isWall(self, xorig, yorig):
        shortestX = 0
        shortestY = 0
        shortestPath = 5

        block_hit_list = pg.sprite.spritecollide(self, self.col_sprites, False)         
        block_hit_list_masked = pg.sprite.spritecollide(self, block_hit_list, False, pg.sprite.collide_mask)        
        if len(block_hit_list_masked) != 0:
        
            for i in range(-5,5):
                for j in range(-5,5):
                    xorigprima = xorig + i
                    yorigprima = yorig + j
                    self.rect = self.image.get_rect(center = (xorigprima, yorigprima))
                    self.mask = pg.mask.from_surface(self.image)            
                    block_hit_list = pg.sprite.spritecollide(self, self.col_sprites, False)         
                    block_hit_list_masked = pg.sprite.spritecollide(self, block_hit_list, False, pg.sprite.collide_mask)        
                    if len(block_hit_list_masked) == 0:
                        if shortestPath > math.sqrt(i**2 + j**2):
                            shortestPath = math.sqrt(i**2 + j**2)
                            shortestX = i * 2
                            shortestY = j * 2
                        
        return shortestX + xorig, shortestY + yorig

    ###########################################################
    # FUNCION UPDATE
    ###########################################################        
    def update(self, player):
        keys = pg.key.get_pressed()

        newX, newY = self.isWall(self.x, self.y)
        self.x =  newX        
        self.y = newY

        if keys[pg.K_a]:
            self.x += self.isBlockX(-1)
        if keys[pg.K_d]:
            self.x += self.isBlockX(1)
        if keys[pg.K_w]:
            self.y += self.isBlockY(-1)
        if keys[pg.K_s]:
            self.y += self.isBlockY(1)
        
        button = pg.mouse.get_pressed()
        (xcursor, ycursor) = pg.mouse.get_pos()
        sen = ycursor - player.rect.centery
        cos = xcursor - player.rect.centerx


        if keys[pg.K_LSHIFT]:
            self.anglehit = 0
            self.blocking = True
            self.swingleft = False
            self.swingright = False
            self.slashright = False
            self.slashleft = False
            self.backleft = False
            self.backright = False
            self.clashright = False
            self.clashleft = False
            self.hitorient = 2
            self.chargecount = 1
            self.countlimit = 0
            self.clash_count = 0
            
        else:
            self.blocking = False
            
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
                        self.anglehit = 270 - angle_grad - self.chargecount * 3  # 3 grados tick
                        self.chargecount += 1
                    if button[2] == 0:
                        self.countlimit = self.chargecount                        
                        self.slashright = True
                        self.swingright = False
                    else:
                        self.anglehit = 270 - angle_grad - self.chargecount * 3                        
                elif self.slashright and not self.swingright and not self.backright:
                    if self.chargecount >= self.countlimit * -20 / 30:
                            self.anglehit = 270 - angle_grad - self.chargecount * 3
                            self.chargecount -= self.isClash(angle_grad, -1, 270)
                    else:
                        self.slashright = False                
                        self.backright = True
                elif self.backright:
                    if self.chargecount <= 1:
                        self.anglehit = 270 - angle_grad - self.chargecount * 3
                        self.chargecount += 1    
                    else:                 
                        self.backright = False
                        self.chargecount = 1
                elif self.clashright:
                    if self.chargecount <= self.clash_count + 20:
                        self.anglehit = 270 - angle_grad - self.chargecount * 3
                        self.chargecount += 1
                    else:                
                        self.clash_count = 0
                        self.chargecount = 1
                        self.clashright = False
                    
                ###########################################################              
                # ESPADAZO DESDE LA IZQUIERDA
                ###########################################################
                if self.swingleft:
                    if self.chargecount <= 30:
                        self.anglehit = 270 - angle_grad + self.chargecount * 3
                        self.chargecount += 1
                    if button[0] == 0:
                        self.countlimit = self.chargecount
                        self.slashleft = True
                        self.swingleft = False   
                    else:
                        self.anglehit = 270 - angle_grad + self.chargecount * 3                        
                elif self.slashleft and not self.swingleft and not self.backleft:
                    if self.chargecount >= self.countlimit * -20 / 30:
                            self.anglehit = 270 - angle_grad + self.chargecount * 3
                            self.chargecount -= self.isClash(angle_grad, 1, 270)                
                    else:
                        self.slashleft = False                
                        self.backleft = True
                elif self.backleft:
                    if self.chargecount <= 1:
                        self.anglehit = 270 - angle_grad + self.chargecount * 3
                        self.chargecount += 1    
                    else:                 
                        self.backleft = False
                        self.chargecount = 1
                elif self.clashleft:
                    if self.chargecount <= self.clash_count + 20:
                        self.anglehit = 270 - angle_grad + self.chargecount * 3
                        self.chargecount += 1
                    else:                
                        self.clash_count = 0
                        self.chargecount = 1
                        self.clashleft = False
                
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
                        self.anglehit = 90 - angle_grad - self.chargecount * 3
                        self.chargecount += 1
                    if button[2] == 0:
                        self.countlimit = self.chargecount                        
                        self.slashright = True
                        self.swingright = False   
                    else:
                        self.anglehit = 90 - angle_grad - self.chargecount * 3
                elif self.slashright and not self.swingright and not self.backright:
                    if self.chargecount >= self.countlimit * -20 / 30:
                            self.anglehit = 90 - angle_grad - self.chargecount * 3
                            self.chargecount -= self.isClash(angle_grad, -1, 90)
                    else:
                        self.slashright = False                
                        self.backright = True
                elif self.backright:
                    if self.chargecount <= 1:
                        self.anglehit = 90 - angle_grad - self.chargecount * 3
                        self.chargecount += 1    
                    else:                 
                        self.backright = False
                        self.chargecount = 1
                elif self.clashright:
                    if self.chargecount <= self.clash_count + 20:
                        self.anglehit = 90 - angle_grad - self.chargecount * 3
                        self.chargecount += 1
                    else:                
                        self.clash_count = 0
                        self.chargecount = 1
                        self.clashright = False
                    
                ###########################################################              
                # ESPADAZO DESDE LA IZQUIERDA
                ###########################################################
                if self.swingleft:
                    if self.chargecount <= 30:
                        self.anglehit = 90 - angle_grad + self.chargecount * 3
                        self.chargecount += 1
                    if button[0] == 0:
                        self.countlimit = self.chargecount                        
                        self.slashleft = True
                        self.swingleft = False    
                    else:
                        self.anglehit = 90 - angle_grad + self.chargecount * 3                        
                elif self.slashleft and not self.swingleft and not self.backleft:
                    if self.chargecount >= self.countlimit * -20 / 30:
                            self.anglehit = 90 - angle_grad + self.chargecount * 3
                            self.chargecount -= self.isClash(angle_grad, 1, 90)               
                    else:
                        self.slashleft = False                
                        self.backleft = True
                elif self.backleft:
                    if self.chargecount <= 1:
                        self.anglehit = 90 - angle_grad + self.chargecount * 3
                        self.chargecount += 1    
                    else:                 
                        self.backleft = False
                        self.chargecount = 1
                elif self.clashleft:
                    if self.chargecount <= self.clash_count + 20:
                        self.anglehit = 90 - angle_grad + self.chargecount * 3
                        self.chargecount += 1
                    else:                
                        self.clash_count = 0
                        self.chargecount = 1
                        self.clashleft = False
                
        ######################################################################
        # HITO CON DIVISION INFINITO, CUADRANTE SUPERIOR
        ######################################################################
        elif cos == 0 and sen < 0:
            self.angle = 0
            angle_grad = 0           
            
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
                    self.anglehit = 0 - self.chargecount * 3
                    self.chargecount += 1
                if button[2] == 0:
                    self.countlimit = self.chargecount                    
                    self.slashright = True
                    self.swingright = False     
                else:
                    self.anglehit = 0 - self.chargecount * 3                    
            elif self.slashright and not self.swingright and not self.backright:
                if self.chargecount >= self.countlimit * -20 / 30:
                        self.anglehit = 0 - self.chargecount * 3
                        self.chargecount -= self.isClash(angle_grad, -1, 0) 
                else:
                    self.slashright = False                
                    self.backright = True
            elif self.backright:
                if self.chargecount <= 1:
                    self.anglehit = 0 - self.chargecount * 3
                    self.chargecount += 1    
                else:                 
                    self.backright = False
                    self.chargecount = 1
                
            ###########################################################              
            # ESPADAZO DESDE LA IZQUIERDA
            ###########################################################
            if self.swingleft:
                if self.chargecount <= 30:
                    self.anglehit = 0 + self.chargecount * 3
                    self.chargecount += 1
                if button[0] == 0:
                    self.countlimit = self.chargecount                                        
                    self.slashleft = True
                    self.swingleft = False       
                else:
                    self.anglehit = 0 + self.chargecount * 3                    
            elif self.slashleft and not self.swingleft and not self.backleft:
                if self.chargecount >= self.countlimit * -20 / 30:
                        self.anglehit = 0 + self.chargecount * 3
                        self.chargecount -= self.isClash(angle_grad, 1, 0)                
                else:
                    self.slashleft = False                
                    self.backleft = True
            elif self.backleft:
                if self.chargecount <= 1:
                    self.anglehit = 0 + self.chargecount * 3
                    self.chargecount += 1    
                else:                 
                    self.backleft = False
                    self.chargecount = 1
            
        ######################################################################
        # HITO CON DIVISION INFINITO, CUADRANTE INFERIOR
        ######################################################################
        elif cos == 0 and sen > 0:
            self.angle = 180
            angle_grad = 0           
            
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
                    self.anglehit = 180 - self.chargecount * 3
                    self.chargecount += 1
                if button[2] == 0:
                    self.countlimit = self.chargecount                                                         
                    self.slashright = True
                    self.swingright = False  
                else:
                    self.anglehit = 180 - self.chargecount * 3                      
            elif self.slashright and not self.swingright and not self.backright:
                if self.chargecount >= self.countlimit * -20 / 30:
                        self.anglehit = 180 - self.chargecount * 3
                        self.chargecount -= self.isClash(angle_grad, -1, 180)
                else:
                    self.slashright = False                
                    self.backright = True
            elif self.backright:
                if self.chargecount <= 1:
                    self.anglehit = 180 - self.chargecount * 3
                    self.chargecount += 1    
                else:                 
                    self.backright = False
                    self.chargecount = 1
                
            ###########################################################              
            # ESPADAZO DESDE LA IZQUIERDA
            ###########################################################
            if self.swingleft:
                if self.chargecount <= 30:
                    self.anglehit = 180 + self.chargecount * 3
                    self.chargecount += 1
                if button[0] == 0:
                    self.countlimit = self.chargecount                    
                    self.slashleft = True
                    self.swingleft = False  
                else:
                    self.anglehit = 180 + self.chargecount * 3                                            
            elif self.slashleft and not self.swingleft and not self.backleft:
                if self.chargecount >= self.countlimit * -20 / 30:
                        self.anglehit = 180 + self.chargecount * 3
                        self.chargecount -= self.isClash(angle_grad, 1, 180)                
                else:
                    self.slashleft = False                
                    self.backleft = True
            elif self.backleft:
                if self.chargecount <= 1:
                    self.anglehit = 180 + self.chargecount * 3
                    self.chargecount += 1    
                else:                 
                    self.backleft = False
                    self.chargecount = 1
        
        self.image = pg.transform.rotate(self.image_orig, self.angle)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.mask = pg.mask.from_surface(self.image)                  

            
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
            self.mask = pg.mask.from_surface(self.image)                  
            
        def update(self, player):
            self.image = pg.transform.rotate(self.image_orig, player.anglehit)
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect(center = player.rect.center)
            self.mask = pg.mask.from_surface(self.image)                  
    
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
            self.mask = pg.mask.from_surface(self.image)                  
            
        def update(self, player):
            self.image = pg.transform.rotate(self.image_orig, player.angle)
            self.image.set_colorkey(BLACK)            
            self.rect = self.image.get_rect(center = player.rect.center)
            self.mask = pg.mask.from_surface(self.image)                  
    
    class sword(pg.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pg.Surface((50,120))
            pg.draw.rect(self.image, RED, (40,0,5,50))
            self.rect = self.image.get_rect(center = (150,150))
            self.image.set_colorkey(BLACK)        
            self.image_orig = self.image
            self.mask = pg.mask.from_surface(self.image)                  

        def update(self, player):
            if player.blocking:
                self.image2 = pg.Surface((120,50))
                pg.draw.rect(self.image2, RED, (30,0,50,5))
                self.image2_orig = self.image2
                self.image = pg.transform.rotate(self.image2_orig, player.angle)
                self.image.set_colorkey(BLACK)            
                self.rect = self.image.get_rect(center = player.rect.center)
                self.mask = pg.mask.from_surface(self.image2)                  
                
            
            else:
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
       
