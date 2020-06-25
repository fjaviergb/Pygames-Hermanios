import pygame as pg

pg.init()

class char(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.radio = 20
        self.image = pg.Surface((50,50))
        pg.draw.rect(self.image, (WHITE), (0,0,50,50))
        pg.draw.circle(self.image, (BLACK), (25,25), self.radio)
        self.rect = self.image.get_rect(center = (150,150))
    
class hand(pg.sprite.Sprite):
    def __init__(self, ori):
        super().__init__()
        self.hittin = False
        self.radio = 10
        self.handspeed = 1
        self.hitcount = 10
        self.ori = ori
        self.image = pg.Surface((20,20))
        pg.draw.rect(self.image, (WHITE), (0,0,20,20))
        self.image.set_colorkey(WHITE)
        if ori == 1:
            pg.draw.circle(self.image, (BLUE), (10,10), self.radio)
            self.rect = self.image.get_rect(topleft = (player.rect.topleft))
        else:
           pg.draw.circle(self.image, (GREEN), (10,10), self.radio)
           self.rect = self.image.get_rect(topright = (player.rect.topright))
   
    def update(self):  
        if self.hittin:
            if self.hitcount > 0:
                self.rect.centery -= self.handspeed
                self.hitcount -= 1
            elif self.hitcount <= 0 and self.hitcount > -10:
                self.rect.centery += self.handspeed
                self.hitcount -= 1
            else:
                self.hitcount = 10
                self.hittin = False

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
      
        button = pg.mouse.get_pressed()
        print(button)
        if button[0] != 0:
            if event.type == pg.MOUSEBUTTONDOWN:            
                Rhand.hittin = True
        if button[2] != 0:
            if event.type == pg.MOUSEBUTTONDOWN:            
                Lhand.hittin = True
    
    all_sprites.update()
    bg.fill(WHITE)
    all_sprites.draw(bg)
    pg.display.update()

pg.quit()