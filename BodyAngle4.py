import pygame as pg
import math
pg.init()

class char(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.radio = 20
        self.image = pg.Surface((50,50))
        pg.draw.rect(self.image, (WHITE), (0,0,50,50))
        pg.draw.circle(self.image, (BLACK), (25,25), self.radio)
        self.rect = self.image.get_rect(center = (150,150))
        self.image_orig = self.image
        self.angle = 0
        self.angle_change = 45

    def update(self):
        self.image = pg.transform.rotate(self.image_orig, self.angle)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect(center=self.rect.center)
    
class hand(pg.sprite.Sprite):
    def __init__(self, ori):
        super().__init__()
        self.hittin = False
        self.angle = 0
        self.dis_max = 0
        self.angle_change = 45
        self.radio = 10
        self.handspeed = 1
        self.hitcount = 5
        self.ori = ori
        self.image = pg.Surface((50,50))
        pg.draw.rect(self.image, (WHITE), (0,0,50,50))
        self.image.set_colorkey(WHITE)
        self.image_orig = self.image
        if ori == 1:
            pg.draw.circle(self.image, (BLUE), (10,10), self.radio)
            self.rect = self.image.get_rect(center = player.rect.center)
        else:
           pg.draw.circle(self.image, (GREEN), (40,10), self.radio)
           self.rect = self.image.get_rect(center = player.rect.center)
   
    def update(self):  
        if self.hittin:
            self.dis = math.sqrt((self.xthrow - player.rect.centerx) ** 2 + (self.ythrow - player.rect.centery) ** 2)
            if self.dis_max < 15:
                self.ratio = self.dis_max / self.dis
                self.rect.centerx = player.rect.centerx + self.ratio * (self.xthrow - player.rect.centerx)
                self.rect.centery = player.rect.centery + self.ratio * (self.ythrow - player.rect.centery) 
                self.dis_max += 2
            else:
                self.dis_max = 0
                self.rect.center = player.rect.center  
                self.hittin = False
                
        self.image = pg.transform.rotate(self.image_orig, self.angle)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect(center=self.rect.center)

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
GOLD = (255,215,0)

player = char()
Rhand = hand(1)
Lhand = hand(0)

all_sprites = pg.sprite.Group()
char_group = pg.sprite.Group()
all_sprites.add(player, Rhand, Lhand)

screen_size = (300,300)
bg = pg.display.set_mode(screen_size)
pg.display.set_caption('Full Body')
clock = pg.time.Clock()
run = True
while run:
    clock.tick(50)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            
        (xcursor, ycursor) = pg.mouse.get_pos()
        button = pg.mouse.get_pressed()
        
        if button[0] != 0:
            if event.type == pg.MOUSEBUTTONDOWN:
                Rhand.hittin = True
                Rhand.xthrow = xcursor
                Rhand.ythrow = ycursor
                            
        if button[2] != 0:
            if event.type == pg.MOUSEBUTTONDOWN:  
                Lhand.hittin = True
                Lhand.xthrow = xcursor
                Lhand.ythrow = ycursor
                
        sen = ycursor - player.rect.centery
        cos = xcursor - player.rect.centerx
        if cos > 0 and sen > 0:
            angle_rad = math.atan(sen / cos)
            angle_grad = angle_rad * 360 / (2 * math.pi)
            player.angle = 270 - angle_grad
            Rhand.angle = 270 - angle_grad
            Lhand.angle = 270 - angle_grad

        elif cos < 0 and sen > 0:
            angle_rad = math.atan(sen / cos)
            angle_grad = angle_rad * 360 / (2 * math.pi)
            player.angle = 90 - angle_grad
            Rhand.angle = 90 - angle_grad
            Lhand.angle = 90 - angle_grad

        elif cos < 0 and sen < 0:
            angle_rad = math.atan(sen / cos)
            angle_grad = angle_rad * 360 / (2 * math.pi)
            player.angle = 90 - angle_grad
            Rhand.angle = 90 - angle_grad
            Lhand.angle = 90 - angle_grad

        elif cos > 0 and sen < 0:
            angle_rad = math.atan(sen / cos)
            angle_grad = angle_rad * 360 / (2 * math.pi)
            player.angle = 180 + (90 - angle_grad)
            Rhand.angle = 180 + (90 - angle_grad)
            Lhand.angle = 180 + (90 - angle_grad)
            
    all_sprites.update()
    bg.fill(WHITE)
    all_sprites.draw(bg)
    pg.display.update()

pg.quit()