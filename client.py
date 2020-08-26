import pygame as pg
from network import Network
from SuperPlayer import body
from otherplayer import otherbody
import otherenvironment as env
from random import randrange
from variables import *

win = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Client")


def main():
    run = True
    p = body(randrange(500), randrange(500))
    all_sprites = pg.sprite.Group()

    all_sprites.add(p)
    all_sprites.add(p.rightH)
    all_sprites.add(p.leftH)
    all_sprites.add(p.espada)
    all_sprites.add(p.livebar)
    all_sprites.add(p.energybar)
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
            (
                p.tipo,
                p.x,
                p.y,
                p.angle,
                p.anglehit,
                p.slashright,
                p.slashleft,
                p.live,
                p.chargecount,
                p.blocking,
            )
        )

        win.fill((255, 255, 255))

        for i in pothers:
            # Dibujamos los contrincantes
            if type(i) != list:
                if (p.x, p.y) != (i[1], i[2]) and i[7] > 0:
                    # Si no eres tu y tiene vida
                    po = otherbody(
                        i[0],  # Tipo de objeto
                        i[1],  # Coordenada x
                        i[2],  # Coordenada y
                        i[3],  # Angle body
                        i[4],  # Anglehit sword
                        i[5],  # Slashright
                        i[6],  # Slashleft
                        i[7],  # Live
                        i[8],  # Chargecount
                        i[9],  # Blocking
                        p.x,   # Posicion cliente x
                        p.y,   # Posicion cliente y
                    )
                    if p.x - 550 < i[1] < p.x + 550 and p.y - 550 < i[2] < p.y + 550:

                        p.other_sprites.add(po)
                        p.other_sprites.add(po.Rhand)
                        p.other_sprites.add(po.Lhand)
                        p.other_sprites.add(po.espada)
                        p.other_sprites.update(po)
                        p.other_sprites.draw(win)
                        if i[5] or i[6]:
                            p.enem_sword.add(po.espada)

                        p.col_sprites.add(po)

                        if i[9] or i[6] or i[5]:
                            p.col_sprites.add(po.espada)

                        p.other_sprites = pg.sprite.Group()

            else:
                #  Colision con el medio ambiente
                for j in i:
                    if j[0] == 4:
                        if (
                            p.x - 550 < j[3] < p.x + 550
                            and p.y - 550 < j[4] < p.y + 550
                        ):

                            envir = env.circle_obstacle(
                                j[1], j[2], j[3], j[4], p.x, p.y
                            )
                            p.env_sprites.add(envir)
                            p.col_sprites.add(envir)

                    elif j[0] == 3:
                        if (
                            p.x - 550 < j[3] < p.x + 550
                            and p.y - 550 < j[4] < p.y + 550
                        ):
                            envir = env.rect_obstacle(j[1], j[2], j[3], j[4], p.x, p.y)
                            p.env_sprites.add(envir)
                            p.col_sprites.add(envir)

                    elif j[0] == 2:
                        if (
                            p.x - 550 < j[3] < p.x + 550
                            and p.y - 550 < j[4] < p.y + 550
                        ):
                            envir = env.gir_obstacle(j[1], j[2], j[3], j[4], p.x, p.y)
                            p.env_sprites.add(envir)
                            p.col_sprites.add(envir)

                    p.env_sprites.draw(win)
                p.env_sprites = pg.sprite.Group()

        if p.live > 0:
            all_sprites.update(p)
            p.col_sprites = pg.sprite.Group()
            p.enem_sword = pg.sprite.Group()
            all_sprites.draw(win)

        pg.display.update()


main()
