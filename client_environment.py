import pygame as pg
from network import Network
import environment
from variables import *

win = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Client")


def main():
    run = True
    border_rect = environment.rect_obstacle(150, 150)

    all_sprites = pg.sprite.Group()
    all_sprites.add(border_rect)


    n = Network()

    clock = pg.time.Clock()

    while run:
        clock.tick(100)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                n.send(False)
                n.client.close()
                run = False
                pg.quit()

        pothers = n.send(
            [
                (border_rect.tipo, 1, 5, border_rect.x, border_rect.y),
            ]
        )

        win.fill((255, 255, 255))

        all_sprites.update()
        all_sprites.draw(win)

        pg.display.update()


main()
