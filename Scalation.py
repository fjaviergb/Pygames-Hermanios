import pygame as pg
from pygame import gfxdraw

pg.init()

class superficie(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, color, colorkey,centerx,centery):
        super().__init__()       
        self.image = pg.Surface((width,height))
        
        pg.draw.rect(self.image, color, (x,y,width - 10,height - 10))
        self.rect = self.image.get_rect(center = (centerx,centery))
        if colorkey:
            self.image.set_colorkey(BLACK)
        
class circle(pg.sprite.Sprite):
    def __init__(self,w,h,r,x,y):
        super().__init__()
        self.image = pg.Surface((2*w,2*h))
        pg.gfxdraw.filled_circle(self.image,w,h,r - 5 ,RED)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center = (x,y))
        
    def update(self):
        self.image = pg.transform.scale(self.image,(40,40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center = (250,250))
        
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
GOLD = (255,215,0)

screen_size = (500,500)
bg = pg.display.set_mode(screen_size)
pg.display.set_caption('Scalation')


circulo = circle(500,500,500,250,250)
all_sprites = pg.sprite.Group()
all_sprites.add(circulo)

circulo2 = pg.Surface((50,50))
pg.gfxdraw.filled_circle(circulo2,25,25,20,RED)
circulo2.set_colorkey(BLACK)

circulo3 = pg.Surface((50,50))
pg.gfxdraw.circle(circulo3,25,25,20,RED)
circulo3.set_colorkey(BLACK)
 
circulo4 = pg.Surface((50,50))
circulo4.fill(WHITE)
pg.gfxdraw.aacircle(circulo4,25,25,20,RED)
pg.gfxdraw.filled_circle(circulo4,25,25,20,RED)
pg.gfxdraw.aacircle(circulo4,25,25,21,BLACK)
pg.gfxdraw.aacircle(circulo4,25,25,22,BLACK)
circulo4.set_colorkey(WHITE)

espada = pg.image.load('espada.png')
espada2 = pg.transform.scale(espada,(50,50))

espada3 = pg.image.load('espada2.png') 
espada4 = pg.transform.smoothscale(espada3,(50,50))

clock = pg.time.Clock()

run = True
while run:
    clock.tick(50)
  
    for event in pg.event.get():
    
        if event.type == pg.QUIT:
            run = False

            
    bg.fill(WHITE)  
    bg.blit(circulo2,(100,100))
    bg.blit(circulo3,(350,350))
    bg.blit(circulo4,(350,50))
    bg.blit(espada,(75,350))
    bg.blit(espada2,(50,350))
    bg.blit(espada3,(50,50))
    bg.blit(espada4,(250,450))
    
    all_sprites.update()
    all_sprites.draw(bg)
    pg.display.update()
    
pg.quit()
