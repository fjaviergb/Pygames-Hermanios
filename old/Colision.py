import pygame as pg

pg.init()


class char(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((50, 50))
        pg.draw.circle(self.image, CPLAYER, (25, 25), 25)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=(250, 250))
        self.mask = pg.mask.from_surface(self.image)
        self.movex = 0
        self.movey = 0

    def update(self):
        self.rect.x += self.movex

        block_hit_list = pg.sprite.spritecollide(self, obstacle_group, False)
        print(block_hit_list)
        block_hit_list_masked = pg.sprite.spritecollide(
            self, block_hit_list, False, pg.sprite.collide_mask
        )
        for block in block_hit_list_masked:

            if type(block) == rect_obstacle:
                if self.movex > 0:
                    self.rect.right += -self.movex
                # =============================================================================
                #                 import pdb
                #                 pdb.set_trace()
                # =============================================================================
                elif self.movex < 0:
                    self.rect.left += -self.movex
                else:
                    pass
            else:
                if self.movex > 0 and self.rect.centery < block.rect.centery:
                    self.rect.top += -3
                elif self.movex > 0 and self.rect.centery > block.rect.centery:
                    self.rect.top += 3

                elif self.movex < 0 and self.rect.centery < block.rect.centery:
                    self.rect.bottom += -3
                elif self.movex < 0 and self.rect.centery > block.rect.centery:
                    self.rect.bottom += 3
                else:
                    pass

        self.rect.y += self.movey
        block_hit_list = pg.sprite.spritecollide(self, obstacle_group, False)
        block_hit_list_masked = pg.sprite.spritecollide(
            self, block_hit_list, False, pg.sprite.collide_mask
        )
        for block in block_hit_list_masked:
            if type(block) == rect_obstacle:
                if self.movey > 0:
                    self.rect.bottom += -self.movey
                elif self.movey < 0:
                    self.rect.top += -self.movey
                else:
                    pass
            else:
                if self.movey > 0 and self.rect.centerx > block.rect.centerx:
                    self.rect.right += 3
                elif self.movey > 0 and self.rect.centerx < block.rect.centerx:
                    self.rect.right += -3
                elif self.movey < 0 and self.rect.centerx > block.rect.centerx:
                    self.rect.left += 3
                elif self.movey < 0 and self.rect.centerx < block.rect.centerx:
                    self.rect.left += -3
                else:
                    pass


class rect_obstacle(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((100, 50))
        self.image.fill(BLUE)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=(100, 100))
        self.mask = pg.mask.from_surface(self.image)


class circle_obstacle(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((150, 150))
        pg.draw.circle(self.image, BLUE, (75, 75), 75)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=(350, 150))
        self.mask = pg.mask.from_surface(self.image)


CBASE = (255, 255, 255)
CPLAYER = (255, 228, 181)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)

screenSize = (500, 500)
bg = pg.display.set_mode(screenSize)
pg.display.set_caption("Medieval Surviv.io")

player = char()
player_group = pg.sprite.Group()
player_group.add(player)

wall = rect_obstacle()
rect_obstacle_group = pg.sprite.Group()
rect_obstacle_group.add(wall)

column = circle_obstacle()
circle_obstacle_group = pg.sprite.Group()
circle_obstacle_group.add(column)

obstacle_group = pg.sprite.Group()
obstacle_group.add(wall)
obstacle_group.add(column)

all_sprites = pg.sprite.Group()
all_sprites.add(player)
all_sprites.add(wall)
all_sprites.add(column)

clock = pg.time.Clock()
run = True
while run:
    clock.tick(50)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                player.movex = -3
            elif event.key == pg.K_RIGHT:
                player.movex = 3
            elif event.key == pg.K_UP:
                player.movey = -3
            elif event.key == pg.K_DOWN:
                player.movey = 3

        elif event.type == pg.KEYUP:
            if event.key == pg.K_LEFT and player.movex < 0:
                player.movex = 0
            elif event.key == pg.K_RIGHT and player.movex > 0:
                player.movex = 0
            elif event.key == pg.K_UP and player.movey < 0:
                player.movey = 0
            elif event.key == pg.K_DOWN and player.movey > 0:
                player.movey = 0

    all_sprites.update()
    bg.fill(BLACK)
    all_sprites.draw(bg)

    pg.display.update()

pg.quit()
