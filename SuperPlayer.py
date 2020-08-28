import pygame as pg
import math
import numpy as np
from otherplayer import otherbody
from utils import is_swinging, sword_movement, sprite_collision
import variables as vars


###########################################################
# CLASE
###########################################################
class body(pg.sprite.Sprite):
    def __init__(self, xinit, yinit):
        super().__init__()
        self.radio = vars.BODY_RADIO
        self.x = xinit
        self.y = yinit
        self.body_image = pg.image.load("HELMET.png")
        self.image = pg.Surface((vars.BODY_IMG_WIDTH, vars.BODY_IMG_HEIGHT))
        self.image.blit(self.body_image, (0,0))
        self.rect = self.image.get_rect(center=(vars.HALF_SCREEN_X, vars.HALF_SCREEN_Y))
        self.mask = pg.mask.from_surface(self.image)
        self.image.set_colorkey(BLACK)
        self.image_orig = self.image
        self.movex = 0
        self.movey = 0
        self.angle = 0
        self.anglehit = 0
        self.swingleft = False
        self.swingright = False
        self.slashright = False
        self.slashleft = False
        self.backleft = False
        self.backright = False
        self.clashright = False
        self.clashleft = False
        self.hitorient = 2
        self.hittin = False
        self.chargecount = 1
        self.countlimit = 0
        self.clash_count = 0
        self.other_sprites = pg.sprite.Group()
        self.col_sprites = pg.sprite.Group()
        self.enem_sword = pg.sprite.Group()
        self.rightH = self.Rhand(xinit, yinit)
        self.leftH = self.Lhand(xinit, yinit)
        self.espada = self.sword(xinit, yinit)
        self.livebar = self.livebar()
        self.energybar = self.energybar()
        self.tipo = 1
        self.env_sprites = pg.sprite.Group()
        self.blocking = False
        self.dashing = False
        self.xdash = 0
        self.ydash = 0
        self.dashcount = 0
        self.dashCD = False
        self.ratio = 0
        self.dashCDcounter = 0
        self.xorigdash = 0
        self.yorigdash = 0
        self.dash_timer = pg.time.get_ticks()
        self.live = vars.LIVEINIT
        self.energy = vars.ENERGYMAX

    ###########################################################
    # FUNCION RECEPCION DAÑO
    ###########################################################
    def ouch(self):
        block_hit_list_masked = sprite_collision(self, None, "enem_sword")

        for block in block_hit_list_masked:
            self.live -= 1
            xclash, yclash = pg.sprite.collide_mask(self, block)
            # print(xclash, self.x, self.rect.width / 2)
            print(xclash + self.x - self.rect.width / 2, yclash + self.y - self.rect.height / 2, block.anglehit)

    ###########################################################
    # FUNCION RECEPCION DAÑO
    ###########################################################
    def toma(self):
        if (self.slashleft and not self.swingleft and not self.backleft) or (
                self.slashright and not self.swingright and not self.backright
        ):
            block_hit_list_masked = sprite_collision(self, "espada", "col_sprites")
            for block in block_hit_list_masked:
                xclash, yclash = pg.sprite.collide_mask(self.espada, block)
                print(xclash + self.x - self.espada.rect.width / 2, yclash + self.y - self.espada.rect.height / 2,
                      self.anglehit)
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

    ###########################################################
    # FUNCION AVANCE DASH
    ###########################################################
    def dis_tic(self):
        """Avoids that the character might enter into objects."""
        for i in range(vars.DISMAX_TIC):
            ratio = (self.dashcount + i) / self.dis
            x = self.xorigdash + ratio * (self.xdash - self.xorigdash)
            y = self.yorigdash + ratio * (self.ydash - self.yorigdash)
            self.rect = self.image.get_rect(center=(x - self.x + vars.HALF_SCREEN_X, y - self.y + vars.HALF_SCREEN_Y))
            block_hit_list_masked = sprite_collision(self, None, "col_sprites")
            if len(block_hit_list_masked) != 0:
                self.dashCD = True
                return i - vars.DIS_SECURE

        return i

    ###########################################################
    # FUNCION COLISION ESPADA
    ###########################################################
    def sword_collision(self, angle_grad, signo, angle, counter):
        #  Metodo para depurar la colision en movimiento.
        #  Como dos objetos en "movimiento" pueden superponerse sin llegar a colisionar
        #  hacemos un pequenno barrido de los angulos para ver si se encuentran.
        for i in np.arange(1, 15, 1):
            #  TODO si el objeto es pequenno puede fallar.
            self.chargecount = counter - i
            self.anglehit = angle - angle_grad + signo * (self.chargecount) * vars.APT_SWORD
            self.espada.image = pg.transform.rotate(
                self.espada.image_orig, self.anglehit
            )
            self.espada.rect = self.espada.image.get_rect(center=self.rect.center)
            self.espada.mask = pg.mask.from_surface(self.espada.image)
            if self.espada.image != self.espada.image_orig and (
                    (self.slashleft and not self.swingleft and not self.backleft)
                    or (self.slashright and not self.swingright and not self.backright)
            ):
                block_hit_list_masked = sprite_collision(self, "espada", "col_sprites")
                if len(block_hit_list_masked) != 0:
                    break

    ###########################################################
    # FUNCION COLISION CUERPO
    ###########################################################
    def body_collision(self, mult, signo, xorig, yorig, is_block_x: bool, is_block_y: bool):
        for i in np.arange(0, mult * vars.VELOCITY, 1):
            if is_block_x:
                self.x = xorig + i * signo
            elif is_block_y:
                self.y = yorig + i * signo
            self.rect = self.image.get_rect(
                center=(self.x - xorig + vars.HALF_SCREEN_X, self.y - yorig + vars.HALF_SCREEN_Y)
            )
            self.mask = pg.mask.from_surface(self.image)

            block_hit_list_masked = sprite_collision(self, None, "col_sprites")
            if len(block_hit_list_masked) != 0:
                if is_block_x:
                    self.x = xorig + (i - 1) * signo
                elif is_block_y:
                    self.y = yorig + (i - 1) * signo
                break

    ###########################################################
    # FUNCION COLISION EN PARADO
    ###########################################################
    def isWall(self, xorig, yorig):
        shortestX = 0
        shortestY = 0
        shortestPath = 5

        block_hit_list_masked = sprite_collision(self, None, "col_sprites")
        if block_hit_list_masked:
            for i in range(-5, 5):
                for j in range(-5, 5):
                    xorigprima = xorig + i
                    yorigprima = yorig + j
                    self.rect = self.image.get_rect(center=(xorigprima, yorigprima))
                    self.mask = pg.mask.from_surface(self.image)
                    block_hit_list_masked = sprite_collision(self, None, "col_sprites")
                    if not block_hit_list_masked:
                        if shortestPath > math.sqrt(i ** 2 + j ** 2):
                            shortestPath = math.sqrt(i ** 2 + j ** 2)
                            shortestX = i * 2
                            shortestY = j * 2

        return shortestX + xorig, shortestY + yorig

    ###########################################################
    # FUNCION UPDATE
    ###########################################################
    def update(self, player):
        self.ouch()
        self.toma()

        keys = pg.key.get_pressed()
        button = pg.mouse.get_pressed()
        (xcursor, ycursor) = pg.mouse.get_pos()
        sen = ycursor - self.rect.centery
        cos = xcursor - self.rect.centerx

        ######################################################################
        # MOVIMIENTO POR COLISIÓN CON OBJETOS
        ######################################################################
        newX, newY = self.isWall(self.x, self.y)
        self.x = newX
        self.y = newY

        ######################################################################
        # DASH CON SPACE
        ######################################################################
        if keys[pg.K_SPACE] and not self.dashing and not self.dashCD:
            self.dashing = True
            self.xdash = xcursor + self.x - vars.HALF_SCREEN_X
            self.ydash = ycursor + self.y - vars.HALF_SCREEN_Y
            self.xorigdash = self.x
            self.yorigdash = self.y
            self.dis = math.sqrt(
                (self.xdash - self.x) ** 2 + (self.ydash - self.y) ** 2
            )

        if self.dashing:
            # Avanza 8 / dis por tic y lo hace 10 veces
            # y comprueba a cada 1 /dis comprueba si choca y de ser asi
            # el objeto queda a una distancia de 2/dis del choque.
            if self.dashcount < vars.DISMAX and self.dashcount < self.dis:
                self.dashcount += self.dis_tic()
                self.ratio = self.dashcount / self.dis
                self.x = self.xorigdash + self.ratio * (self.xdash - self.xorigdash)
                self.y = self.yorigdash + self.ratio * (self.ydash - self.yorigdash)
                if self.dashCD:
                    self.dashcount = 0
                    self.dashing = False
            else:
                self.dash_timer = pg.time.get_ticks()
                self.dashCD = True
                self.dashcount = 0
                self.dashing = False

        ######################################################################
        # MOVIMIENTO A-S-D-W; CORRIENDO CON CTRL
        ######################################################################
        else:
            if keys[pg.K_a]:
                if keys[pg.K_LCTRL] and self.energy > 0:
                    self.body_collision(2, -1, self.x, self.y, True, False)
                else:
                    self.body_collision(1, -1, self.x, self.y, True, False)
            if keys[pg.K_d]:
                if keys[pg.K_LCTRL] and self.energy > 0:
                    self.body_collision(2, 1, self.x, self.y, True, False)
                else:
                    self.body_collision(1, 1, self.x, self.y, True, False)
            if keys[pg.K_w]:
                if keys[pg.K_LCTRL] and self.energy > 0:
                    self.body_collision(2, -1, self.x, self.y, False, True)
                else:
                    self.body_collision(1, -1, self.x, self.y, False, True)
            if keys[pg.K_s]:
                if keys[pg.K_LCTRL] and self.energy > 0:
                    self.body_collision(2, 1, self.x, self.y, False, True)
                else:
                    self.body_collision(1, 1, self.x, self.y, False, True)

            if self.dashCD:
                if pg.time.get_ticks() - self.dash_timer > vars.DASH_CD:
                    self.dashcount = 0
                    self.dashCD = False

        if (
                keys[pg.K_LSHIFT]
                and not self.slashleft
                and not self.backleft
                and not self.slashright
                and not self.backright
        ):
            self.anglehit = 0
            self.blocking = True
            self.swingleft = False
            self.swingright = False
            self.slashright = False
            self.slashleft = False
            self.backleft = False
            self.backright = False
            self.clashright = False
            self.clashleft = False
            self.hitorient = 2
            self.chargecount = 1
            self.countlimit = 0
            self.clash_count = 0

        else:
            self.blocking = False

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
                self.angle = 270 - angle_grad
                if (
                        button[2] != 0
                        and not is_swinging(self)):
                    self.hitorient = 1
                    self.swingright = True
                    self.anglehit = self.angle - 90
                elif (
                        button[0] != 0
                        and not is_swinging(self)):
                    self.hitorient = 0
                    self.swingleft = True
                    self.anglehit = self.angle + 90
                elif (
                        button[2] == 0
                        and button[0] == 0
                        and not is_swinging(self)):
                    self.anglehit = self.angle

                ###########################################################
                # ESPADAZO DESDE LA DERECHA
                ###########################################################
                sword_movement(self, "swingright", -1, button[2], "slashright", 270, "backright", angle_grad,
                               "clashright")

                ###########################################################
                # ESPADAZO DESDE LA IZQUIERDA
                ###########################################################
                sword_movement(self, "swingleft", 1, button[0], "slashleft", 270, "backleft", angle_grad, "clashleft")

            ######################################################################
            # CUADRANTE IZQUIERDA
            ######################################################################
            elif cos < 0:
                self.angle = 90 - angle_grad
                if (
                        button[2] != 0
                        and not is_swinging(self)):
                    self.hitorient = 1
                    self.swingright = True
                    self.anglehit = self.angle - 90
                elif (
                        button[0] != 0
                        and not is_swinging(self)):
                    self.hitorient = 0
                    self.swingleft = True
                    self.anglehit = self.angle + 90
                elif (
                        button[2] == 0
                        and button[0] == 0
                        and not is_swinging(self)):
                    self.anglehit = self.angle

                ###########################################################
                # ESPADAZO DESDE LA DERECHA
                ###########################################################
                sword_movement(self, "swingright", -1, button[2], "slashright", 90, "backright", angle_grad,
                               "clashright")

                ###########################################################
                # ESPADAZO DESDE LA IZQUIERDA
                ###########################################################
                sword_movement(self, "swingleft", 1, button[0], "slashleft", 90, "backleft", angle_grad, "clashleft")

        ######################################################################
        # HITO CON DIVISION INFINITO, CUADRANTE SUPERIOR
        ######################################################################
        elif cos == 0 and sen < 0:
            self.angle = 0
            angle_grad = 0

            if (
                    button[2] != 0
                    and not is_swinging(self)):
                self.hitorient = 1
                self.swingright = True
            elif (
                    button[0] != 0
                    and not is_swinging(self)):
                self.hitorient = 0
                self.swingleft = True

            ###########################################################
            # ESPADAZO DESDE LA DERECHA
            ###########################################################
            sword_movement(self, "swingright", -1, button[2], "slashright", 0, "backright", angle_grad, "clashright")

            ###########################################################
            # ESPADAZO DESDE LA IZQUIERDA
            ###########################################################
            sword_movement(self, "swingleft", 1, button[0], "slashleft", 0, "backleft", angle_grad, "clashleft")


        ######################################################################
        # HITO CON DIVISION INFINITO, CUADRANTE INFERIOR
        ######################################################################
        elif cos == 0 and sen > 0:
            self.angle = 180
            angle_grad = 0

            if (
                    button[2] != 0
                    and not is_swinging(self)):
                self.hitorient = 1
                self.swingright = True
            elif (
                    button[0] != 0
                    and not is_swinging(self)):
                self.hitorient = 0
                self.swingleft = True

            ###########################################################
            # ESPADAZO DESDE LA DERECHA
            ###########################################################
            sword_movement(self, "swingright", -1, button[2], "slashright", 180, "backright", angle_grad, "clashright")

            ###########################################################
            # ESPADAZO DESDE LA IZQUIERDA
            ###########################################################
            sword_movement(self, "swingleft", 1, button[0], "slashleft", 180, "backleft", angle_grad, "clashleft")

        if keys[pg.K_LCTRL] and self.energy > 0:
            self.energy -= vars.EPT_RUN
        if self.energy < vars.ENERGYMAX:
            self.energy += vars.EPT_RECOVER

        self.image = pg.transform.rotate(self.image_orig, self.angle)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=(vars.HALF_SCREEN_X, vars.HALF_SCREEN_Y))
        self.mask = pg.mask.from_surface(self.image)

    class Rhand(pg.sprite.Sprite):
        def __init__(self, xinit, yinit):
            super().__init__()
            self.image = pg.Surface((vars.HAND_IMG_WIDTH, vars.HAND_IMG_HEIGHT))
            self.image.set_colorkey(BLACK)
            pg.draw.circle(self.image, (GOLD), (vars.BODY_IMG_WIDTH - vars.HAND_RADIO, vars.HAND_RADIO), vars.HAND_RADIO)
            self.rect = self.image.get_rect(center=(xinit, yinit))
            self.image_orig = self.image
            self.mask = pg.mask.from_surface(self.image)

        def update(self, player):
            self.image = pg.transform.rotate(self.image_orig, player.anglehit)
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect(center=player.rect.center)
            self.mask = pg.mask.from_surface(self.image)

    class Lhand(pg.sprite.Sprite):
        def __init__(self, xinit, yinit):
            super().__init__()
            self.image = pg.Surface((vars.HAND_IMG_WIDTH, vars.HAND_IMG_HEIGHT))
            self.image.set_colorkey(BLACK)
            pg.draw.circle(self.image, (GOLD), (vars.HAND_RADIO, vars.HAND_RADIO), vars.HAND_RADIO)
            self.rect = self.image.get_rect(center=(xinit, yinit))
            self.image_orig = self.image
            self.mask = pg.mask.from_surface(self.image)

        def update(self, player):
            self.image = pg.transform.rotate(self.image_orig, player.angle)
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect(center=player.rect.center)
            self.mask = pg.mask.from_surface(self.image)

    class sword(pg.sprite.Sprite):
        def __init__(self, xinit, yinit):
            super().__init__()
            self.sword_image = pg.image.load("SWORD.png")
            self.sword_image_gir = pg.image.load("SWORD_GIR.png")
            self.image = pg.Surface((vars.SWORD_IMG_WIDTH, vars.SWORD_IMG_HEIGHT))
            self.image.blit(self.sword_image, (vars.BODY_IMG_WIDTH - vars.HAND_RADIO - int(vars.SWORD_WIDTH / 2), int(vars.SWORD_IMG_HEIGHT / 2) - (vars.SWORD_HEIGHT + int(vars.BODY_IMG_HEIGHT / 2) - vars.HAND_RADIO)))
            self.rect = self.image.get_rect(center=(xinit, yinit))
            self.image.set_colorkey(BLACK)
            self.image_orig = self.image
            self.mask = pg.mask.from_surface(self.image)

        def update(self, player):
            if player.blocking:
                self.image2 = pg.Surface((120, 50))  # TODO: still hardcoded
                self.image2.blit(self.sword_image_gir, (30,0))
                self.image2_orig = self.image2
                self.image = pg.transform.rotate(self.image2_orig, player.angle)
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect(center=player.rect.center)
                self.mask = pg.mask.from_surface(self.image)

            else:
                self.image = pg.transform.rotate(self.image_orig, player.anglehit)
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect(center=player.rect.center)
                self.mask = pg.mask.from_surface(self.image)

    class livebar(pg.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pg.Surface((vars.LIVEBAR_WIDTH, vars.LIVEBAR_HEIGHT))
            pg.draw.rect(self.image, RED, (0, 0, vars.LIVEBAR_WIDTH, vars.LIVEBAR_HEIGHT))
            self.rect = self.image.get_rect(topleft=(vars.LIVEBAR_TOPLEFT_X, vars.LIVEBAR_TOPLEFT_Y))

        def update(self, player):
            pg.draw.rect(self.image, RED, (0, 0, vars.LIVEBAR_WIDTH, vars.LIVEBAR_HEIGHT))
            pg.draw.rect(self.image, GREEN, (0, 0, player.live / vars.LIVEINIT * vars.LIVEBAR_WIDTH, vars.LIVEBAR_HEIGHT))
            self.rect = self.image.get_rect(topleft=(vars.LIVEBAR_TOPLEFT_X, vars.LIVEBAR_TOPLEFT_Y))

    class energybar(pg.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pg.Surface((vars.ENERGYBAR_WIDTH, vars.ENERGYBAR_HEIGHT))
            pg.draw.rect(self.image, GOLD, (1, 1, vars.ENERGYBAR_WIDTH - vars.ENERGYBAR_BLACK_BORDER, vars.ENERGYBAR_HEIGHT - vars.ENERGYBAR_BLACK_BORDER))
            self.rect = self.image.get_rect(topleft=(vars.ENERGYBAR_TOPLEFT_X, vars.ENERGYBAR_TOPLEFT_Y))

        def update(self, player):
            pg.draw.rect(self.image, BLACK, (0, 0, vars.ENERGYBAR_WIDTH, vars.ENERGYBAR_HEIGHT))
            pg.draw.rect(self.image, GOLD, (1, 1, player.energy / vars.ENERGYMAX * (vars.ENERGYBAR_WIDTH - vars.ENERGYBAR_BLACK_BORDER), vars.ENERGYBAR_HEIGHT - vars.ENERGYBAR_BLACK_BORDER))
            self.rect = self.image.get_rect(topleft=(vars.ENERGYBAR_TOPLEFT_X, vars.ENERGYBAR_TOPLEFT_Y))


CBASE = (255, 255, 255)
CPLAYER = (255, 228, 181)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)
WHITE = (255, 255, 255)
