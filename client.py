import pygame as pg
from network import Network
from SuperPlayer import body
from otherplayer import otherbody

width = 500
height = 500
win = pg.display.set_mode((width, height))
pg.display.set_caption("Client")


def main():
    run = True
    p = body()
    all_sprites = pg.sprite.Group()
    all_sprites.add(p)
    all_sprites.add(p.Rhand())
    all_sprites.add(p.Lhand())
    all_sprites.add(p.sword())
    n = Network()
    
    clock = pg.time.Clock()
    print(type(all_sprites))
    while run:
        clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                n.send(False)  
                n.client.close()
                run = False
                pg.quit()

        pothers = n.send((p.x,p.y,p.angle,p.anglehit))

        win.fill((255,255,255))
        
        for i in pothers:
            po = otherbody(i[0],i[1],i[2],i[3])
            other_sprites = pg.sprite.Group()
            other_sprites.add(po)
            other_sprites.add(po.otherRhand())
            other_sprites.add(po.otherLhand())
            other_sprites.add(po.othersword()) 
            other_sprites.update(po)
            other_sprites.draw(win)
            
        all_sprites.update(p)
        all_sprites.draw(win)
        pg.display.update()

main()