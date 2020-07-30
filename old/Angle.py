import pygame as pg
import math

pg.init()


class rect(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 50
        self.height = 100
        self.image = pg.Surface((self.width, self.height))
        self.image.fill(WHITE)
        pg.draw.rect(self.image, (BLACK), (1, 1, 48, 98))
        pg.draw.circle(self.image, (WHITE), (5, 5), 2)
        self.image.set_colorkey(WHITE)
        self.image_orig = self.image
        self.rect = self.image.get_rect(center=(150, 150))
        self.angle = 0
        self.angle_change = 45

    def update(self):
        self.image = pg.transform.rotate(self.image_orig, self.angle)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect(center=self.rect.center)


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

player = rect()
all_sprites = pg.sprite.Group()
all_sprites.add(player)

clock = pg.time.Clock()
run = True

screen_size = (300, 300)
bg = pg.display.set_mode(screen_size)
pg.display.set_caption("Angles")

while run:
    clock.tick(50)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        # =============================================================================
        #         elif event.type == pg.KEYDOWN:
        #             if event.key == pg.K_LEFT:
        #                 player.angle += player.angle_change
        #             elif event.key == pg.K_RIGHT:
        #                 player.angle -= player.angle_change
        #
        # =============================================================================
        (xcursor, ycursor) = pg.mouse.get_pos()
        sen = ycursor - player.rect.centery
        cos = xcursor - player.rect.centerx
        if cos > 0 and sen > 0:
            angle_rad = math.atan(sen / cos)
            angle_grad = angle_rad * 360 / (2 * math.pi)
            player.angle = 270 - angle_grad
        elif cos < 0 and sen > 0:
            angle_rad = math.atan(sen / cos)
            angle_grad = angle_rad * 360 / (2 * math.pi)
            player.angle = 90 - angle_grad
        elif cos < 0 and sen < 0:
            angle_rad = math.atan(sen / cos)
            angle_grad = angle_rad * 360 / (2 * math.pi)
            player.angle = 90 - angle_grad
        elif cos > 0 and sen < 0:
            angle_rad = math.atan(sen / cos)
            angle_grad = angle_rad * 360 / (2 * math.pi)
            player.angle = 180 + (90 - angle_grad)

    all_sprites.update()
    pg.display.update()
    bg.fill(WHITE)
    all_sprites.draw(bg)

pg.quit()
