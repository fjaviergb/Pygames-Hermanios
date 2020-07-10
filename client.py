import pygame as pg
from network import Network
from SuperPlayer import body

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
    print(all_sprites)
    while run:
        clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                n.send(False)  
                n.client.close()
                run = False
                pg.quit()

        all_sprites.update(p)
        pothers = n.send(p) 
                        
    win.fill((255,255,255))
    for p in pothers:
        p.draw()
    pg.display.update()

main()