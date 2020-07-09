import pygame as pg
import math

pg.init()

class char(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.radio = 20
        self.image = pg.Surface((50,50))
        self.image.set_colorkey(BLACK)        
        pg.draw.circle(self.image, (WHITE), (25,25), self.radio)
        self.rect = self.image.get_rect(center = (150,150))
        self.image_orig = self.image
        self.angle = 0
        self.angle_change = 45

    def update(self):
        self.image = pg.transform.rotate(self.image_orig, self.angle)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=self.rect.center)

class hand(pg.sprite.Sprite):
    def __init__(self, ori):
        super().__init__()
        self.angle = 0
        self.angle_change = 45
        self.radio = 10
        self.handspeed = 1
        self.hitcount = 10
        self.ori = ori
        self.image = pg.Surface((50,50))
        self.image.set_colorkey(BLACK)
        self.image_orig = self.image
        if ori == 1:
            pg.draw.circle(self.image, (BLUE), (10,10), self.radio)
            self.rect = self.image.get_rect(center = player.rect.center)
        else:
           pg.draw.circle(self.image, (GREEN), (40,10), self.radio)
           self.rect = self.image.get_rect(center = player.rect.center)

    def update(self):           
        self.image = pg.transform.rotate(self.image_orig, self.angle)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=self.rect.center)


class sword(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((50,120))
        self.image.set_colorkey(BLACK)
        pg.draw.line(self.image, RED, (43,35), (50,0), 5)
        self.rect = self.image.get_rect(center = (150,150))
        self.image_orig = self.image
        self.angle = 0
        self.angle_change = 45
        self.chargecount = 1
        self.swingright = False
        self.swingleft = False
        self.slashright = False
        self.slashleft = False
        self.backright= False
        self.backleft = False
        self.cursorcount = 0
        self.cursor_dir = 0
        self.leftbut = 2

    def update(self):
        self.image = pg.transform.rotate(self.image_orig, self.angle)
        self.rect = self.image.get_rect(center = player.rect.center)


CBASE = (255,255,255)
CPLAYER = (255,228,181)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
GOLD = (255,215,0)
WHITE = (255,255,255)

screen_size = (500,400)
bg = pg.display.set_mode(screen_size)
pg.display.set_caption('Espadas')

player = char()
Rhand = hand(1)
Lhand = hand(0)
espada = sword()

all_sprites = pg.sprite.Group()
all_sprites.add(player)
all_sprites.add(Rhand)
all_sprites.add(Lhand)
all_sprites.add(espada)

cursorcount = 0
clock = pg.time.Clock()
run = True
while run:
    clock.tick(50)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            
        button = pg.mouse.get_pressed()
        (xcursor, ycursor) = pg.mouse.get_pos()
        sen = ycursor - player.rect.centery
        cos = xcursor - player.rect.centerx
                        
        if cos != 0:
            angle_rad = math.atan(sen / cos)
            angle_grad = angle_rad * 360 / (2 * math.pi)
            
            if cos > 0:
                player.angle = 270 - angle_grad
                Rhand.angle = 270 - angle_grad
                if button[0] != 0 and espada.cursor_dir > 40:
                    espada.leftbut = 1                                        
                    espada.swingright = True
                    Lhand.angle = 270 - angle_grad - 90
                    espada.angle = 270 - angle_grad - 90  
                elif button[0] != 0 and espada.cursor_dir < -40:
                    espada.leftbut = 0           
                    espada.swingleft = True
                    Lhand.angle = 270 - angle_grad + 90
                    espada.angle = 270 - angle_grad + 90               
                else:
                    espada.swingright = False 
                    espada.swingleft = False
                    Lhand.angle = 270 - angle_grad
                    espada.angle = 270 - angle_grad                                 
                    
            elif cos < 0:
                player.angle = 90 - angle_grad
                Rhand.angle = 90 - angle_grad
                if button[0] != 0 and espada.cursor_dir > 40:
                    espada.leftbut = 1                    
                    espada.swingright = True                
                    Lhand.angle = 90 - angle_grad - 90
                    espada.angle = 90 - angle_grad - 90  
                elif button[0] != 0 and espada.cursor_dir < -40:
                    espada.leftbut = 0           
                    espada.swingleft = True
                    Lhand.angle = 90 - angle_grad + 90
                    espada.angle = 90 - angle_grad + 90               
                    
                else:
                    espada.swingright = False
                    espada.swingleft = False
                    Lhand.angle = 90 - angle_grad
                    espada.angle = 90 - angle_grad
        
        elif cos == 0 and sen < 0:
            angle_grad = 0
            if button[0] != 0 and espada.cursor_dir > 40:
                espada.leftbut = 1
                espada.swingright = True 
            elif button[0] != 0 and espada.cursor_dir < -40:
                espada.leftbut = 0                           
                espada.swingleft = True
            else:
                espada.swingright = False
                espada.swingleft = False
        
        elif cos == 0 and sen > 0:
            angle_grad = 180
            if button[0] != 0 and espada.cursor_dir > 40:
                espada.leftbut = 1                                   
                espada.swingright = True 
            elif button[0] != 0 and espada.cursor_dir < -40:
                espada.leftbut = 0                          
                espada.swingleft = True                
            else:
                espada.swingright = False
                espada.swingleft = False
     
        # SOLTAR EL RATON COMIENZA EL SLASH
        if event.type == pg.MOUSEBUTTONUP:
            if espada.leftbut == 1:
                espada.slashright = True
                espada.leftbut = 2
            elif espada.leftbut == 0:
                espada.slashleft = True
                espada.leftbut = 2
                
    if espada.cursorcount == 0:
        cursor_init = xcursor
        espada.cursorcount += 1            
    elif espada.cursorcount > 0 and espada.cursorcount <= 5:
        espada.cursorcount += 1
    elif not espada.swingright and not espada.swingleft:        
        espada.cursor_dir = xcursor - cursor_init
        espada.cursorcount = 0
#    print(espada.cursor_dir, cursor_init)

# ESPADAZO
    if cos < 0:
        # ESPADAZO DESDE DERECHA
        if espada.swingright:
            if espada.chargecount <= 30:
                Lhand.angle = 90 - angle_grad - espada.chargecount * 90 / 30
                espada.angle = 90 - angle_grad - espada.chargecount * 90 / 30
                espada.chargecount += 1
        elif espada.slashright and not espada.swingright and not espada.backright:
            if espada.chargecount >= -20:
                Lhand.angle = 90 - angle_grad - espada.chargecount * 90 / 30
                espada.angle = 90 - angle_grad - espada.chargecount * 90 / 30
                espada.chargecount -= 8  
            else:
                espada.slashright = False                
                espada.backright = True
        elif espada.backright:
            if espada.chargecount <= 1:
                Lhand.angle = 90 - angle_grad - espada.chargecount * 90 / 30
                espada.angle = 90 - angle_grad - espada.chargecount * 90 / 30
                espada.chargecount += 1    
            else:                 
                espada.backright = False
                espada.chargecount = 1
                
        # ESPADAZO DESDE IZQUIERDA                
        if espada.swingleft:
            if espada.chargecount <= 30:
                Lhand.angle = 90 - angle_grad + espada.chargecount * 90 / 30
                espada.angle = 90 - angle_grad + espada.chargecount * 90 / 30
                espada.chargecount += 1
        elif espada.slashleft and not espada.swingleft and not espada.backleft:
            if espada.chargecount >= -20:
                Lhand.angle = 90 - angle_grad + espada.chargecount * 90 / 30
                espada.angle = 90 - angle_grad + espada.chargecount * 90 / 30
                espada.chargecount -= 8  
            else:
                espada.slashleft = False                
                espada.backleft = True
        elif espada.backleft:
            if espada.chargecount <= 1:
                Lhand.angle = 90 - angle_grad + espada.chargecount * 90 / 30
                espada.angle = 90 - angle_grad + espada.chargecount * 90 / 30
                espada.chargecount += 1    
            else:                 
                espada.backleft = False
                espada.chargecount = 1
                
    if cos > 0:
        # ESPADAZO DESDE DERECHA        
        if espada.swingright:
            if espada.chargecount <= 30:
                Lhand.angle = 270 - angle_grad - espada.chargecount * 90 / 30
                espada.angle = 270 - angle_grad - espada.chargecount * 90 / 30
                espada.chargecount += 1
        elif espada.slashright and not espada.swingright and not espada.backright:
            if espada.chargecount >= -20:
                Lhand.angle = 270 - angle_grad - espada.chargecount * 90 / 30
                espada.angle = 270 - angle_grad - espada.chargecount * 90 / 30
                espada.chargecount -= 8    
            else:
                espada.slashright = False                
                espada.backright = True
        elif espada.backright:
            if espada.chargecount <= 1:
                Lhand.angle = 270 - angle_grad - espada.chargecount * 90 / 30
                espada.angle = 270 - angle_grad - espada.chargecount * 90 / 30
                espada.chargecount += 1    
            else: 
                espada.backright = False
                espada.chargecount = 1
                
        # ESPADAZO DESDE IZQUIERDA
        if espada.swingleft:
            if espada.chargecount <= 30:
                Lhand.angle = 270 - angle_grad + espada.chargecount * 90 / 30
                espada.angle = 270 - angle_grad + espada.chargecount * 90 / 30
                espada.chargecount += 1
        elif espada.slashleft and not espada.swingleft and not espada.backleft:
            if espada.chargecount >= -20:
                Lhand.angle = 270 - angle_grad + espada.chargecount * 90 / 30
                espada.angle = 270 - angle_grad + espada.chargecount * 90 / 30
                espada.chargecount -= 8  
            else:
                espada.slashleft = False                
                espada.backleft = True
        elif espada.backleft:
            if espada.chargecount <= 1:
                Lhand.angle = 270 - angle_grad + espada.chargecount * 90 / 30
                espada.angle = 270 - angle_grad + espada.chargecount * 90 / 30
                espada.chargecount += 1    
            else:                 
                espada.backleft = False
                espada.chargecount = 1

    if cos == 0 and sen < 0:
        
        # ESPADAZO DESDE DERECHA        
        if espada.swingright:
            if espada.chargecount <= 30:
                Lhand.angle = 0 - espada.chargecount * 90 / 30
                espada.angle = 0 - espada.chargecount * 90 / 30
                espada.chargecount += 1
        elif espada.slashright and not espada.swingright and not espada.backright:
            if espada.chargecount >= -20:
                Lhand.angle = 0 - espada.chargecount * 90 / 30
                espada.angle = 0 - espada.chargecount * 90 / 30
                espada.chargecount -= 8    
            else:
                espada.slashright = False                
                espada.backright = True
        elif espada.backright:
            if espada.chargecount <= 1:
                Lhand.angle = 0 - espada.chargecount * 90 / 30
                espada.angle = 0 - espada.chargecount * 90 / 30
                espada.chargecount += 1    
            else: 
                espada.backright = False
                espada.chargecount = 1
                
        # ESPADAZO DESDE IZQUIERDA
        if espada.swingleft:
            if espada.chargecount <= 30:
                Lhand.angle = 0 + espada.chargecount * 90 / 30
                espada.angle = 0 + espada.chargecount * 90 / 30
                espada.chargecount += 1
        elif espada.slashleft and not espada.swingleft and not espada.backleft:
            if espada.chargecount >= -20:
                Lhand.angle = 0 + espada.chargecount * 90 / 30
                espada.angle = 0 + espada.chargecount * 90 / 30
                espada.chargecount -= 8  
            else:
                espada.slashleft = False                
                espada.backleft = True
        elif espada.backleft:
            if espada.chargecount <= 1:
                Lhand.angle = 0 + espada.chargecount * 90 / 30
                espada.angle = 0 + espada.chargecount * 90 / 30
                espada.chargecount += 1    
            else:                 
                espada.backleft = False
                espada.chargecount = 1
    
    if cos == 0 and sen > 0:
        
        # ESPADAZO DESDE DERECHA        
        if espada.swingright:
            if espada.chargecount <= 30:
                Lhand.angle = 180 - espada.chargecount * 90 / 30
                espada.angle = 180 - espada.chargecount * 90 / 30
                espada.chargecount += 1
        elif espada.slashright and not espada.swingright and not espada.backright:
            if espada.chargecount >= -20:
                Lhand.angle = 180 - espada.chargecount * 90 / 30
                espada.angle = 180 - espada.chargecount * 90 / 30
                espada.chargecount -= 8    
            else:
                espada.slashright = False                
                espada.backright = True
        elif espada.backright:
            if espada.chargecount <= 1:
                Lhand.angle = 180 - espada.chargecount * 90 / 30
                espada.angle = 180 - espada.chargecount * 90 / 30
                espada.chargecount += 1    
            else: 
                espada.backright = False
                espada.chargecount = 1
                
        # ESPADAZO DESDE IZQUIERDA               
        if espada.swingleft:
            if espada.chargecount <= 30:
                Lhand.angle = 180 + espada.chargecount * 90 / 30
                espada.angle = 180 + espada.chargecount * 90 / 30
                espada.chargecount += 1
        elif espada.slashleft and not espada.swingleft and not espada.backleft:
            if espada.chargecount >= -20:
                Lhand.angle = 180 + espada.chargecount * 90 / 30
                espada.angle = 180 + espada.chargecount * 90 / 30
                espada.chargecount -= 8  
            else:
                espada.slashleft = False                
                espada.backleft = True
        elif espada.backleft:
            if espada.chargecount <= 1:
                Lhand.angle = 180 + espada.chargecount * 90 / 30
                espada.angle = 180 + espada.chargecount * 90 / 30
                espada.chargecount += 1    
            else:                 
                espada.backleft = False
                espada.chargecount = 1

#    print(espada.swingright, espada.slashright, espada.backright, espada.chargecount)
    all_sprites.update()
    bg.fill(BLACK)
    all_sprites.draw(bg)
    pg.display.update()
pg.quit()