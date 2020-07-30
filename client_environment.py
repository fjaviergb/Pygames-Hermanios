import pygame as pg
from network import Network
import environment

width = 500
height = 500
win = pg.display.set_mode((width, height))
pg.display.set_caption("Client")


def main():
    run = True
    gir = environment.gir_obstacle(80, 300)
    rect = environment.rect_obstacle(75, 50)
    cir = environment.circle_obstacle(350, 150)
    rect2 = environment.rect_obstacle(1500, 1550)
    rect3 = environment.rect_obstacle(500, 2500)
    rect4 = environment.rect_obstacle(2500, 500)
    rect5 = environment.rect_obstacle(2500, 2500)

    all_sprites = pg.sprite.Group()
    all_sprites.add(gir)
    all_sprites.add(rect)
    all_sprites.add(cir)
    all_sprites.add(rect2)
    all_sprites.add(rect3)
    all_sprites.add(rect4)
    all_sprites.add(rect5)

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

        pothers = n.send(
            [
                (gir.tipo, gir.counter, gir.live, gir.x, gir.y),
                (rect.tipo, rect.counter, rect.live, rect.x, rect.y),
                (cir.tipo, cir.counter, cir.live, cir.x, cir.y),
                (rect2.tipo, rect2.counter, rect2.live, rect2.x, rect2.y),
                (rect3.tipo, rect3.counter, rect3.live, rect3.x, rect3.y),
                (rect4.tipo, rect4.counter, rect4.live, rect4.x, rect4.y),
                (rect5.tipo, rect5.counter, rect5.live, rect5.x, rect5.y),
            ]
        )

        win.fill((255, 255, 255))

        all_sprites.update()
        all_sprites.draw(win)

        pg.display.update()


main()
