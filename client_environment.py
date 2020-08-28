import pygame as pg
from network import Network
import environment

def main():
    run = True
    border_rect = environment.rect_obstacle(150, 150)

    all_sprites = pg.sprite.Group()
    all_sprites.add(border_rect)

    clock = pg.time.Clock()

    while run:
        clock.tick(100)
        pothers = n.send(
            [
                (border_rect.tipo, 1, 5, border_rect.x, border_rect.y),
            ]
        )

        all_sprites.update()

n = Network()

try:
    main()
except:
    n.send(False)
    n.client.close()
    run = False
