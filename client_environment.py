import pygame as pg
from network import Network
from SuperPlayer import body
from otherplayer import otherbody
import environment


width = 500
height = 500
win = pg.display.set_mode((width, height))
pg.display.set_caption("Client")

def main():
    run = True
    gir = environment.gir_obstacle()
    rect = environment.rect_obstacle()
    cir = environment.circle_obstacle()
    
    all_sprites = pg.sprite.Group()
    all_sprites.add(gir)
    all_sprites.add(rect)
    all_sprites.add(cir)

    n = Network()
    
    clock = pg.time.Clock()

    while run:
        clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                n.send(False)  
                n.client.close()
                run = False
                pg.quit()

        pothers = n.send([(gir.tipo,gir.counter,gir.live),(rect.tipo,rect.counter,rect.live),(cir.tipo,cir.counter,cir.live)])

        win.fill((255,255,255))
                
        all_sprites.update()
        all_sprites.draw(win)

        pg.display.update()

main()