import pygame as pg
import math
import numpy as np

pg.init()

##################################################################
# CLASE OBSTÁCULO
##################################################################
class gir_obstacle(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.live = 6
        self.image = pg.Surface((50, 150))
        pg.draw.rect(self.image, BLUE, (20, 25, 10, 100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=(80, 300))
        self.mask = pg.mask.from_surface(self.image)
        self.image_orig = self.image
        self.counter = 0
        self.crash = False

    def update(self):
        if not self.crash:
            if self.counter <= 360:
                self.image = pg.transform.rotate(self.image_orig, 8 * self.counter)
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect(center=self.rect.center)
                self.mask = pg.mask.from_surface(self.image)
                self.counter += 1
            else:
                self.counter = 0
        else:
            pass

        pg.draw.rect(self.image, (RED), (10, 0, 60, 5))
        pg.draw.rect(self.image, (GREEN), (10, 0, self.live * 10, 5))

        if self.live <= 0:
            self.image.fill(BLACK)
            self.image.set_colorkey(BLACK)
            obstacle_group.remove(self)


##################################################################
# CLASE OBSTÁCULO RECTANGULAR
##################################################################
class rect_obstacle(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((100, 50))
        pg.draw.rect(self.image, BLUE, (5, 5, 90, 40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=(75, 50))
        self.mask = pg.mask.from_surface(self.image)
        self.live = 3

    def update(self):
        pg.draw.rect(self.image, (RED), (10, 0, 30, 5))
        pg.draw.rect(self.image, (GREEN), (10, 0, self.live * 10, 5))

        if self.live <= 0:
            self.image.fill(BLACK)
            self.image.set_colorkey(BLACK)
            obstacle_group.remove(self)


##################################################################
# CLASE OBSTÁCULO CIRCULAR
##################################################################
class circle_obstacle(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((150, 150))
        pg.draw.circle(self.image, BLUE, (75, 75), 75)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=(350, 150))
        self.mask = pg.mask.from_surface(self.image)
        self.live = 3

    def update(self):
        pg.draw.rect(self.image, (RED), (10, 0, 30, 5))
        pg.draw.rect(self.image, (GREEN), (10, 0, self.live * 10, 5))

        if self.live <= 0:
            self.image.fill(BLACK)
            self.image.set_colorkey(BLACK)
            obstacle_group.remove(self)


##################################################################
# CLASE CUERPO
##################################################################
class char(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.radio = 20
        self.image = pg.Surface((50, 50))
        pg.draw.circle(self.image, (WHITE), (25, 25), self.radio)
        self.rect = self.image.get_rect(center=(150, 150))
        self.image.set_colorkey(BLACK)
        self.image_orig = self.image
        self.angle = 0
        self.angle_change = 45
        self.movex = 0
        self.movey = 0

    def update(self):
        self.image = pg.transform.rotate(self.image_orig, self.angle)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=self.rect.center)

        ################################
        # MOVIMIENTO HORIZONTAL
        ################################

        self.rect.x += self.movex
        block_hit_list = pg.sprite.spritecollide(self, obstacle_group, False)
        block_hit_list_masked = pg.sprite.spritecollide(
            self, block_hit_list, False, pg.sprite.collide_mask
        )

        for block in block_hit_list_masked:
            if type(block) == circle_obstacle:
                if self.movex > 0 and self.rect.centery < block.rect.centery:
                    self.rect.top += -4
                    Lhand.rect.top += -4
                    Rhand.rect.top += -4
                    espada.rect.top += -4

                elif self.movex > 0 and self.rect.centery > block.rect.centery:
                    self.rect.top += 4
                    Lhand.rect.top += 4
                    Rhand.rect.top += 4
                    espada.rect.top += 4

                elif self.movex < 0 and self.rect.centery < block.rect.centery:
                    self.rect.bottom += -4
                    Lhand.rect.bottom += -4
                    Rhand.rect.bottom += -4
                    espada.rect.bottom += -4

                elif self.movex < 0 and self.rect.centery > block.rect.centery:
                    self.rect.bottom += 4
                    Lhand.rect.bottom += 4
                    Rhand.rect.bottom += 4
                    espada.rect.bottom += 4

                elif self.movex < 0 and self.rect.centery == block.rect.centery:
                    self.rect.left += 3
                    Lhand.rect.left += 3
                    Rhand.rect.left += 3
                    espada.rect.left += 3

                elif self.movex > 0 and self.rect.centery == block.rect.centery:
                    self.rect.left += -3
                    Lhand.rect.left += -3
                    Rhand.rect.left += -3
                    espada.rect.left += -3

            else:
                if self.movex > 0:
                    self.rect.right += -self.movex
                    Lhand.rect.right += -self.movex
                    Rhand.rect.right += -self.movex
                    espada.rect.right += -self.movex

                elif self.movex < 0:
                    self.rect.left += -self.movex
                    Lhand.rect.left += -self.movex
                    Rhand.rect.left += -self.movex
                    espada.rect.left += -self.movex

                else:
                    pass

        ################################
        # MOVIMIENTO VERTICAL
        ################################
        self.rect.y += self.movey
        block_hit_list = pg.sprite.spritecollide(self, obstacle_group, False)
        block_hit_list_masked = pg.sprite.spritecollide(
            self, block_hit_list, False, pg.sprite.collide_mask
        )

        for block in block_hit_list_masked:
            if type(block) == rect_obstacle:
                if self.movey > 0:
                    self.rect.bottom += -self.movey
                    Lhand.rect.bottom += -self.movey
                    Rhand.rect.bottom += -self.movey
                    espada.rect.bottom += -self.movey

                elif self.movey < 0:
                    self.rect.top += -self.movey
                    Lhand.rect.top += -self.movey
                    Rhand.rect.top += -self.movey
                    espada.rect.top += -self.movey

                else:
                    pass
            else:
                if self.movey > 0 and self.rect.centerx > block.rect.centerx:
                    self.rect.right += 4
                    Lhand.rect.right += 4
                    Rhand.rect.right += 4
                    espada.rect.right += 4

                elif self.movey > 0 and self.rect.centerx < block.rect.centerx:
                    self.rect.right += -4
                    Lhand.rect.right += -4
                    Rhand.rect.right += -4
                    espada.rect.right += -4

                elif self.movey < 0 and self.rect.centerx > block.rect.centerx:
                    self.rect.left += 4
                    Lhand.rect.left += 4
                    Rhand.rect.left += 4
                    espada.rect.left += 4

                elif self.movey < 0 and self.rect.centerx < block.rect.centerx:
                    self.rect.left += -4
                    Lhand.rect.left += -4
                    Rhand.rect.left += -4
                    espada.rect.left += -4

                elif self.movey < 0 and self.rect.centerx == block.rect.centerx:
                    self.rect.bottom += -3
                    Lhand.rect.bottom += -3
                    Rhand.rect.bottom += -3
                    espada.rect.bottom += -3

                elif self.movey > 0 and self.rect.centerx == block.rect.centerx:
                    self.rect.bottom += 3
                    Lhand.rect.bottom += 3
                    Rhand.rect.bottom += 3
                    espada.rect.bottom += 3


##################################################################
# CLASE MANOS
##################################################################
class hand(pg.sprite.Sprite):
    def __init__(self, ori):
        super().__init__()
        self.angle = 0
        self.angle_change = 45
        self.radio = 10
        self.handspeed = 1
        self.hitcount = 10
        self.ori = ori
        self.image = pg.Surface((50, 50))
        self.image.set_colorkey(BLACK)
        self.image_orig = self.image
        self.hittin = False
        self.dis_max = 0
        self.movex = 0
        self.movey = 0

        if ori == 1:
            pg.draw.circle(self.image, (BLUE), (10, 10), self.radio)
            self.rect = self.image.get_rect(center=player.rect.center)
        else:
            pg.draw.circle(self.image, (GREEN), (40, 10), self.radio)
            self.rect = self.image.get_rect(center=player.rect.center)

    def update(self):
        self.image = pg.transform.rotate(self.image_orig, self.angle)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=self.rect.center)

        self.rect.x += player.movex
        self.rect.y += player.movey


##################################################################
# CLASE ESPADA
##################################################################
class sword(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((50, 120))
        pg.draw.rect(self.image, RED, (40, 0, 5, 50))
        self.rect = self.image.get_rect(center=(150, 150))
        self.image.set_colorkey(BLACK)
        self.mask = pg.mask.from_surface(self.image)
        self.image_orig = self.image
        self.angle = 0
        self.angle_change = 45
        self.chargecount = 1
        self.swingright = False
        self.swingleft = False
        self.slashright = False
        self.slashleft = False
        self.backright = False
        self.backleft = False
        self.cursorcount = 0
        self.cursor_dir = 0
        self.leftbut = 2
        self.hittin = False
        self.dis_max = 0
        self.movex = 0
        self.movey = 0
        self.countlimit = 0
        self.clashleft = False
        self.clashright = False
        self.last_angle = self.angle
        self.clash_count = 0
        self.cdcount = 0
        self.cd = False

    def update(self):
        self.image = pg.transform.rotate(self.image_orig, self.angle)
        self.rect = self.image.get_rect(center=player.rect.center)

        self.rect.x += player.movex
        self.rect.y += player.movey

        if self.hittin:
            self.dis = math.sqrt(
                (self.xthrow - player.rect.centerx) ** 2
                + (self.ythrow - player.rect.centery) ** 2
            )
            if self.dis_max < 25:
                self.ratio = self.dis_max / self.dis
                self.rect.centerx = player.rect.centerx + self.ratio * (
                    self.xthrow - player.rect.centerx
                )
                Rhand.rect.centerx = player.rect.centerx + self.ratio * (
                    self.xthrow - player.rect.centerx
                )
                self.rect.centery = player.rect.centery + self.ratio * (
                    self.ythrow - player.rect.centery
                )
                Rhand.rect.centery = player.rect.centery + self.ratio * (
                    self.ythrow - player.rect.centery
                )
                self.dis_max += 2
            else:
                self.dis_max = 0
                self.rect.center = player.rect.center
                Rhand.rect.center = player.rect.center
                self.hittin = False
        elif not self.hittin:
            self.dis_max = 0
            self.rect.center = player.rect.center
            Rhand.rect.center = player.rect.center
            self.hittin = False

        if self.image != self.image_orig and (
            (self.slashleft and not self.swingleft and not self.backleft)
            or (self.slashright and not self.swingright and not self.backright)
            or (self.chargecount == 31 and self.swingleft)
            or (self.hittin)
        ):
            self.mask = pg.mask.from_surface(self.image)
            block_hit_list = pg.sprite.spritecollide(self, obstacle_group, False)
            block_hit_list_masked = pg.sprite.spritecollide(
                self, block_hit_list, False, pg.sprite.collide_mask
            )
            for block in block_hit_list_masked:
                if self.slashleft:
                    self.clashleft = True
                    self.clash_count = self.chargecount
                    self.slashleft = False
                    self.backleft = False
                    self.slashright = False
                    self.backright = False
                    self.swingleft = False
                    self.swingright = False
                elif self.slashright:
                    self.clashright = True
                    self.clash_count = self.chargecount
                    self.slashleft = False
                    self.backleft = False
                    self.slashright = False
                    self.backright = False
                    self.swingleft = False
                    self.swingright = False
                elif self.hittin:
                    self.hittin = False

                if type(block) == gir_obstacle:
                    girator.crash = True
                else:
                    girator.crash = False

                if self.chargecount == 31 and self.swingleft:
                    pass
                else:
                    block.live -= 1

        if self.slashleft or self.slashright or self.hittin:
            self.cd = True
        if self.cd and self.cdcount <= 60:
            self.cdcount += 1
        else:
            self.cd = False
            self.cdcount = 0


##############################################################################
# INICIACION DE VARIABLES
##############################################################################
CBASE = (255, 255, 255)
CPLAYER = (255, 228, 181)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)
WHITE = (255, 255, 255)

screen_size = (500, 400)
bg = pg.display.set_mode(screen_size)
pg.display.set_caption("Espadas")

player = char()
Lhand = hand(1)
Rhand = hand(0)
espada = sword()

all_sprites = pg.sprite.Group()
all_sprites.add(player)
all_sprites.add(Lhand)
all_sprites.add(Rhand)
all_sprites.add(espada)

wall = rect_obstacle()
column = circle_obstacle()
girator = gir_obstacle()
obstacle_group = pg.sprite.Group()
obstacle_group.add(wall)
obstacle_group.add(column)
obstacle_group.add(girator)
all_sprites.add(wall)
all_sprites.add(column)
all_sprites.add(girator)

###########################################################
# FUNCION COLISION ESPADA
###########################################################
def isClash(angle_grad, signo, angle):
    #  Metodo para depurar la colision en movimiento.
    #  Como dos objetos en "movimiento" pueden superponerse sin llegar a colisionar
    #  hacemos un pequenno barrido de los angulos para ver si se encuentran.
    for i in np.arange(0, 8, 0.5):
        #  TODO si el objeto es pequenno puede fallar.
        Rhand.angle = angle - angle_grad + signo * (espada.chargecount - i) * 3
        espada.angle = angle - angle_grad + signo * (espada.chargecount - i) * 3
        espada.image = pg.transform.rotate(espada.image_orig, espada.angle)
        espada.rect = espada.image.get_rect(center=player.rect.center)
        espada.mask = pg.mask.from_surface(espada.image)
        if espada.image != espada.image_orig and (
            (espada.slashleft and not espada.swingleft and not espada.backleft)
            or (espada.slashright and not espada.swingright and not espada.backright)
        ):
            block_hit_list = pg.sprite.spritecollide(espada, obstacle_group, False)
            block_hit_list_masked = pg.sprite.spritecollide(
                espada, block_hit_list, False, pg.sprite.collide_mask
            )
            if len(block_hit_list_masked) == 0:
                pass
            else:
                break
        else:
            pass
    return i


##################################################################
# INICIACION DEL BUCLE FUNCIONAMIENTO
##################################################################
cursorcount = 0
clock = pg.time.Clock()
run = True
while run:
    clock.tick(100)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        ##################################################################
        # RESETEO OBJETOS CON LA TECLA Q
        ##################################################################
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                wall = rect_obstacle()
                column = circle_obstacle()
                girator = gir_obstacle()
                obstacle_group.add(wall)
                obstacle_group.add(column)
                obstacle_group.add(girator)
                all_sprites.add(wall)
                all_sprites.add(column)
                all_sprites.add(girator)

        ##################################################################
        # OBTENCIÓN DE POSICIÓN DEL CURSOR Y BOTÓN DEL RATÓN PULSADO
        ##################################################################
        button = pg.mouse.get_pressed()
        (xcursor, ycursor) = pg.mouse.get_pos()
        sen = ycursor - player.rect.centery
        cos = xcursor - player.rect.centerx

        ##################################################################
        # MOVIMIENTO
        ##################################################################
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                player.movex = -3
                espada.movex = -3
                Lhand.movex = -3
                Rhand.movex = -3

            elif event.key == pg.K_RIGHT:
                player.movex = 3
                espada.movex = 3
                Lhand.movex = 3
                Rhand.movex = 3

            elif event.key == pg.K_UP:
                player.movey = -3
                espada.movey = -3
                Lhand.movey = -3
                Rhand.movey = -3

            elif event.key == pg.K_DOWN:
                player.movey = 3
                espada.movey = 3
                Lhand.movey = 3
                Rhand.movey = 3

        elif event.type == pg.KEYUP:
            if event.key == pg.K_LEFT and player.movex < 0:
                player.movex = 0
            elif event.key == pg.K_RIGHT and player.movex > 0:
                player.movex = 0
            elif event.key == pg.K_UP and player.movey < 0:
                player.movey = 0
            elif event.key == pg.K_DOWN and player.movey > 0:
                player.movey = 0

        ######################################################################
        # ROTACIÓN + COMIENZO ESPADAZO
        ######################################################################
        ######################################################################
        # HITO PARA EVITAR DIVISION ENTRE INFINITO
        ######################################################################
        if cos != 0:
            angle_rad = math.atan(sen / cos)
            angle_grad = angle_rad * 360 / (2 * math.pi)

            ######################################################################
            # CUADRANTE DERECHA
            ######################################################################
            if cos > 0:
                player.angle = 270 - angle_grad
                Lhand.angle = 270 - angle_grad
                if button[2] != 0 and not espada.swingleft and not espada.cd:
                    espada.leftbut = 1
                    espada.swingright = True
                    Rhand.angle = 270 - angle_grad - 90
                    espada.angle = 270 - angle_grad - 90
                elif button[0] != 0 and not espada.swingright and not espada.cd:
                    espada.leftbut = 0
                    espada.swingleft = True
                    Rhand.angle = 270 - angle_grad + 90
                    espada.angle = 270 - angle_grad + 90
                else:
                    espada.swingright = False
                    espada.swingleft = False
                    Rhand.angle = 270 - angle_grad
                    espada.angle = 270 - angle_grad
                    if (
                        button[1] != 0
                        and not espada.swingright
                        and not espada.swingleft
                        and not espada.cd
                    ):
                        espada.hittin = True
                        espada.xthrow = xcursor
                        espada.ythrow = ycursor

            ######################################################################
            # CUADRANTE IZQUIERDA
            ######################################################################
            elif cos < 0:
                player.angle = 90 - angle_grad
                Lhand.angle = 90 - angle_grad
                if button[2] != 0 and not espada.swingleft and not espada.cd:
                    espada.leftbut = 1
                    espada.swingright = True
                    Rhand.angle = 90 - angle_grad - 90
                    espada.angle = 90 - angle_grad - 90
                elif button[0] != 0 and not espada.swingright and not espada.cd:
                    espada.leftbut = 0
                    espada.swingleft = True
                    Rhand.angle = 90 - angle_grad + 90
                    espada.angle = 90 - angle_grad + 90
                else:
                    espada.swingright = False
                    espada.swingleft = False
                    Rhand.angle = 90 - angle_grad
                    espada.angle = 90 - angle_grad
                    if (
                        button[1] != 0
                        and not espada.swingright
                        and not espada.swingleft
                        and not espada.cd
                    ):
                        espada.hittin = True
                        espada.xthrow = xcursor
                        espada.ythrow = ycursor

        ######################################################################
        # HITO CON DIVISION INFINITO, CUADRANTE SUPERIOR
        ######################################################################
        elif cos == 0 and sen < 0:
            angle_grad = 0
            if button[2] != 0 and not espada.swingleft and not espada.cd:
                espada.leftbut = 1
                espada.swingright = True
            elif button[0] != 0 and not espada.swingright and not espada.cd:
                espada.leftbut = 0
                espada.swingleft = True
            else:
                espada.swingright = False
                espada.swingleft = False
                if (
                    button[1] != 0
                    and not espada.swingright
                    and not espada.swingleft
                    and not espada.cd
                ):
                    espada.hittin = True
                    espada.xthrow = xcursor
                    espada.ythrow = ycursor

        ######################################################################
        # HITO CON DIVISION INFINITO, CUADRANTE INFERIOR
        ######################################################################
        elif cos == 0 and sen > 0:
            angle_grad = 180
            if button[2] != 0 and not espada.swingleft and not espada.cd:
                espada.leftbut = 1
                espada.swingright = True
            elif button[0] != 0 and not espada.swingright and not espada.cd:
                espada.leftbut = 0
                espada.swingleft = True
            else:
                espada.swingright = False
                espada.swingleft = False
                if (
                    button[1] != 0
                    and not espada.swingright
                    and not espada.swingleft
                    and not espada.cd
                ):
                    espada.hittin = True
                    espada.xthrow = xcursor
                    espada.ythrow = ycursor

        ######################################################################
        # HITO COMIENZO DEL SLASH, SUELTA EL ESPADAZO
        ######################################################################
        if event.type == pg.MOUSEBUTTONUP:
            if espada.leftbut == 1:
                espada.slashright = True
                espada.countlimit = espada.chargecount
                espada.leftbut = 2
            elif espada.leftbut == 0:
                espada.slashleft = True
                espada.countlimit = espada.chargecount
                espada.leftbut = 2

    ###########################################################
    # ESPADAZO
    ###########################################################
    ###########################################################
    # ESPADAZO - CUADRANTE IZQUIERDO
    ###########################################################
    if cos < 0:
        ###########################################################
        # ESPADAZO DESDE LA DERECHA
        ###########################################################
        if espada.swingright:
            if espada.chargecount <= 30:
                Rhand.angle = 90 - angle_grad - espada.chargecount * 90 / 30
                espada.angle = 90 - angle_grad - espada.chargecount * 90 / 30
                espada.chargecount += 1
        elif espada.slashright and not espada.swingright and not espada.backright:
            if espada.chargecount >= espada.countlimit * -20 / 30:
                Rhand.angle = 90 - angle_grad - espada.chargecount * 90 / 30
                espada.angle = 90 - angle_grad - espada.chargecount * 90 / 30
                espada.chargecount -= isClash(angle_grad, -1, 90)
            else:
                espada.slashright = False
                espada.backright = True
        elif espada.backright:
            if espada.chargecount <= 1:
                Rhand.angle = 90 - angle_grad - espada.chargecount * 90 / 30
                espada.angle = 90 - angle_grad - espada.chargecount * 90 / 30
                espada.chargecount += 1
            else:
                espada.backright = False
                espada.chargecount = 1
        elif espada.clashright:
            if espada.chargecount <= espada.clash_count + 10:
                Rhand.angle = 90 - angle_grad - espada.chargecount * 90 / 30
                espada.angle = 90 - angle_grad - espada.chargecount * 90 / 30
                espada.chargecount += 1
            else:
                espada.clash_count = 0
                espada.chargecount = 1
                espada.clashright = False

        ###########################################################
        # ESPADAZO DESDE LA IZQUIERDA
        ###########################################################
        if espada.swingleft:
            if espada.chargecount <= 30:
                Rhand.angle = 90 - angle_grad + espada.chargecount * 90 / 30
                espada.angle = 90 - angle_grad + espada.chargecount * 90 / 30
                espada.chargecount += 1
        elif espada.slashleft and not espada.swingleft and not espada.backleft:
            if espada.chargecount >= espada.countlimit * -20 / 30:
                Rhand.angle = 90 - angle_grad + espada.chargecount * 90 / 30
                espada.angle = 90 - angle_grad + espada.chargecount * 90 / 30
                espada.chargecount -= isClash(angle_grad, 1, 90)
            else:
                espada.slashleft = False
                espada.backleft = True
        elif espada.backleft:
            if espada.chargecount <= 1:
                Rhand.angle = 90 - angle_grad + espada.chargecount * 90 / 30
                espada.angle = 90 - angle_grad + espada.chargecount * 90 / 30
                espada.chargecount += 1
            else:
                espada.backleft = False
                espada.chargecount = 1
        elif espada.clashleft:
            if espada.chargecount <= espada.clash_count + 10:
                Rhand.angle = 90 - angle_grad + espada.chargecount * 90 / 30
                espada.angle = 90 - angle_grad + espada.chargecount * 90 / 30
                espada.chargecount += 1
            else:
                espada.clash_count = 0
                espada.chargecount = 1
                espada.clashleft = False

    ###########################################################
    # ESPADAZO - CUADRANTE DERECHO
    ###########################################################
    if cos > 0:
        ###########################################################
        # ESPADAZO DESDE LA DERECHA
        ###########################################################
        if espada.swingright:
            if espada.chargecount <= 30:
                Rhand.angle = 270 - angle_grad - espada.chargecount * 90 / 30
                espada.angle = 270 - angle_grad - espada.chargecount * 90 / 30
                espada.chargecount += 1
        elif espada.slashright and not espada.swingright and not espada.backright:
            if espada.chargecount >= espada.countlimit * -20 / 30:
                Rhand.angle = 270 - angle_grad - espada.chargecount * 90 / 30
                espada.angle = 270 - angle_grad - espada.chargecount * 90 / 30
                espada.chargecount -= isClash(angle_grad, -1, 270)
            else:
                espada.slashright = False
                espada.backright = True
        elif espada.backright:
            if espada.chargecount <= 1:
                Rhand.angle = 270 - angle_grad - espada.chargecount * 90 / 30
                espada.angle = 270 - angle_grad - espada.chargecount * 90 / 30
                espada.chargecount += 1
            else:
                espada.backright = False
                espada.chargecount = 1
        elif espada.clashright:
            if espada.chargecount <= espada.clash_count + 10:
                Rhand.angle = 270 - angle_grad - espada.chargecount * 90 / 30
                espada.angle = 270 - angle_grad - espada.chargecount * 90 / 30
                espada.chargecount += 1
            else:
                espada.clash_count = 0
                espada.chargecount = 1
                espada.clashright = False

        ###########################################################
        # ESPADAZO DESDE LA IZQUIERDA
        ###########################################################
        if espada.swingleft:
            if espada.chargecount <= 30:
                Rhand.angle = 270 - angle_grad + espada.chargecount * 90 / 30
                espada.angle = 270 - angle_grad + espada.chargecount * 90 / 30
                espada.chargecount += 1
        elif espada.slashleft and not espada.swingleft and not espada.backleft:
            if espada.chargecount >= espada.countlimit * -20 / 30:
                Rhand.angle = 270 - angle_grad + espada.chargecount * 90 / 30
                espada.angle = 270 - angle_grad + espada.chargecount * 90 / 30
                espada.chargecount -= isClash(angle_grad, 1, 270)
            else:
                espada.slashleft = False
                espada.backleft = True
        elif espada.backleft:
            if espada.chargecount <= 1:
                Rhand.angle = 270 - angle_grad + espada.chargecount * 90 / 30
                espada.angle = 270 - angle_grad + espada.chargecount * 90 / 30
                espada.chargecount += 1
            else:
                espada.backleft = False
                espada.chargecount = 1
        elif espada.clashleft:
            if espada.chargecount <= espada.clash_count + 10:
                Rhand.angle = 270 - angle_grad + espada.chargecount * 90 / 30
                espada.angle = 270 - angle_grad + espada.chargecount * 90 / 30
                espada.chargecount += 1
            else:
                espada.clash_count = 0
                espada.chargecount = 1
                espada.clashleft = False

    ###########################################################
    # ESPADAZO - VERTICAL, CUADRANTE SUPERIOR
    ###########################################################
    if cos == 0 and sen < 0:
        ###########################################################
        # ESPADAZO DESDE LA DERECHA
        ###########################################################
        if espada.swingright:
            if espada.chargecount <= 30:
                Rhand.angle = 0 - espada.chargecount * 90 / 30
                espada.angle = 0 - espada.chargecount * 90 / 30
                espada.chargecount += 1
        elif espada.slashright and not espada.swingright and not espada.backright:
            if espada.chargecount >= espada.countlimit * -20 / 30:
                Rhand.angle = 0 - espada.chargecount * 90 / 30
                espada.angle = 0 - espada.chargecount * 90 / 30
                espada.chargecount -= isClash(angle_grad, -1, 0)
            else:
                espada.slashright = False
                espada.backright = True
        elif espada.backright:
            if espada.chargecount <= 1:
                Rhand.angle = 0 - espada.chargecount * 90 / 30
                espada.angle = 0 - espada.chargecount * 90 / 30
                espada.chargecount += 1
            else:
                espada.backright = False
                espada.chargecount = 1

        ###########################################################
        # ESPADAZO DESDE LA IZQUIERDA
        ###########################################################
        if espada.swingleft:
            if espada.chargecount <= 30:
                Rhand.angle = 0 + espada.chargecount * 90 / 30
                espada.angle = 0 + espada.chargecount * 90 / 30
                espada.chargecount += 1
        elif espada.slashleft and not espada.swingleft and not espada.backleft:
            if espada.chargecount >= espada.countlimit * -20 / 30:
                Rhand.angle = 0 + espada.chargecount * 90 / 30
                espada.angle = 0 + espada.chargecount * 90 / 30
                espada.chargecount -= isClash(angle_grad, 1, 0)
            else:
                espada.slashleft = False
                espada.backleft = True
        elif espada.backleft:
            if espada.chargecount <= 1:
                Rhand.angle = 0 + espada.chargecount * 90 / 30
                espada.angle = 0 + espada.chargecount * 90 / 30
                espada.chargecount += 1
            else:
                espada.backleft = False
                espada.chargecount = 1

    ###########################################################
    # ESPADAZO - VERTICAL, CUADRANTE INFERIOR
    ###########################################################
    if cos == 0 and sen > 0:
        ###########################################################
        # ESPADAZO DESDE LA DERECHA
        ###########################################################
        if espada.swingright:
            if espada.chargecount <= 30:
                Rhand.angle = 180 - espada.chargecount * 90 / 30
                espada.angle = 180 - espada.chargecount * 90 / 30
                espada.chargecount += 1
        elif espada.slashright and not espada.swingright and not espada.backright:
            if espada.chargecount >= espada.countlimit * -20 / 30:
                Rhand.angle = 180 - espada.chargecount * 90 / 30
                espada.angle = 180 - espada.chargecount * 90 / 30
                espada.chargecount -= isClash(angle_grad, -1, 180)
            else:
                espada.slashright = False
                espada.backright = True
        elif espada.backright:
            if espada.chargecount <= 1:
                Rhand.angle = 180 - espada.chargecount * 90 / 30
                espada.angle = 180 - espada.chargecount * 90 / 30
                espada.chargecount += 1
            else:
                espada.backright = False
                espada.chargecount = 1

        ###########################################################
        # ESPADAZO DESDE LA IZQUIERDA
        ###########################################################
        if espada.swingleft:
            if espada.chargecount <= 30:
                Rhand.angle = 180 + espada.chargecount * 90 / 30
                espada.angle = 180 + espada.chargecount * 90 / 30
                espada.chargecount += 1
        elif espada.slashleft and not espada.swingleft and not espada.backleft:
            if espada.chargecount >= espada.countlimit * -20 / 30:
                Rhand.angle = 180 + espada.chargecount * 90 / 30
                espada.angle = 180 + espada.chargecount * 90 / 30
                espada.chargecount -= isClash(angle_grad, 1, 180)
            else:
                espada.slashleft = False
                espada.backleft = True
        elif espada.backleft:
            if espada.chargecount <= 1:
                Rhand.angle = 180 + espada.chargecount * 90 / 30
                espada.angle = 180 + espada.chargecount * 90 / 30
                espada.chargecount += 1
            else:
                espada.backleft = False
                espada.chargecount = 1

    ###########################################################
    # ACTUALIZACION DEL DISPLAY
    ###########################################################
    all_sprites.update()
    bg.fill(BLACK)
    all_sprites.draw(bg)
    pg.display.update()

pg.quit()
