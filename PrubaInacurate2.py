import sys
import random
import pygame as pg
import pygame.gfxdraw

pg.init()


class Wall(pg.sprite.Sprite):
    """Wall a player can run into."""
    def __init__(self, x, y, width, height, colour):
        super().__init__()
        self.image = pg.Surface([width, height])
        self.image.fill(colour)
        self.image.set_colorkey(BLACK)
        # Make the "passed-in" location the top left corner.
        self.mask = pg.mask.from_surface(self.image)        
        self.rect = self.image.get_rect(topleft=(x, y))


class Collectable(pg.sprite.Sprite):
    """A collectable item."""

    def __init__(self, colour, x, y, image, rect):
        super().__init__()
        self.image = pg.Surface((5, 5))
        self.image.fill(colour)
        self.rect = self.image.get_rect(topleft=(x, y))


class Player(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30, 30))
#        pg.gfxdraw.aacircle(self.image,15,15,15,(50, 150, 250))
#        pg.gfxdraw.filled_circle(self.image,15,15,15,(50, 150, 250))
        self.image.set_colorkey(BLACK)
        pg.draw.circle(self.image,(50, 150, 250),(15,15),15)
        self.mask = pg.mask.from_surface(self.image)        
        self.rect = self.image.get_rect()
        #SET THE INITIAL SPEED TO ZERO
        self.change_x = 0
        self.change_y = 0
        self.health = 100

    def update(self):
        # Move left/right.
        self.rect.x += self.change_x

        # Did this update cause us to hit a wall?
        block_hit_list = pg.sprite.spritecollide(self, self.walls, False, pg.sprite.collide_mask)
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of
            # the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down.
        self.rect.y += self.change_y
        
        # Check and see if we hit anything.
        block_hit_list = pg.sprite.spritecollide(self, self.walls, False, pg.sprite.collide_mask)
        for block in block_hit_list:
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom


BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
GOLD = (255,215,0)

size = (500, 500)
screen = pg.display.set_mode(size)
pg.display.set_caption("The Life Game")

wall_list = pg.sprite.Group()
all_sprites = pg.sprite.Group()
enemy_list = pg.sprite.Group()
coins = pg.sprite.Group()

player = Player()
player.walls = wall_list
all_sprites.add(player)

for i in range(random.randrange(100,200)):
    x = random.randrange(size[0])
    y = random.randrange(size[1])
    whiteStar = Collectable(WHITE, x, y, "White Star", "Rect")
    all_sprites.add(whiteStar)

for i in range(50):
    x = random.randrange(size[0])
    y = random.randrange(size[1])
    enemy = Collectable(RED, x, y, "Enemy","Ellipse")
    enemy_list.add(enemy)
    all_sprites.add(enemy)

coin1 = Collectable(GOLD,240,200,"Coin","Ellipse")
coin2 = Collectable(GOLD,100,340,"Coin","Ellipse")
all_sprites.add(coin1, coin2)
coins.add(coin1, coin2)

# Make the walls.
walls = [Wall(0,0,10,600,RED), Wall(50, 300, 400, 10,RED),
         Wall(10, 200, 100, 10,RED)]
wall_list.add(walls)
all_sprites.add(walls)


def main():
    clock = pg.time.Clock()
    done = False
    score = 0
    font_score = pg.font.SysFont('Calibri',20,True,False)
    font_health = pg.font.SysFont('Calibri',20,True,False)
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            # Do the movement in the event loop by setting
            # the player's change_x and y attributes.
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    player.change_x = -3
                elif event.key == pg.K_RIGHT:
                    player.change_x = 3
                elif event.key == pg.K_UP:
                    player.change_y = -3
                elif event.key == pg.K_DOWN:
                    player.change_y = 3
            elif event.type == pg.KEYUP:
                if event.key == pg.K_LEFT and player.change_x < 0:
                    player.change_x = 0
                elif event.key == pg.K_RIGHT and player.change_x > 0:
                    player.change_x = 0
                elif event.key == pg.K_UP and player.change_y < 0:
                    player.change_y = 0
                elif event.key == pg.K_DOWN and player.change_y > 0:
                    player.change_y = 0

        # UPDATE SECTION / Put the logic of your game here (i.e. how
        # objects move, when to fire them, etc).
        all_sprites.update()

        # spritecollide returns a list of the collided sprites in the
        # passed group. Iterate over this list to do something per
        # collided sprite. Set dokill argument to True to kill the sprite.
        collided_enemies = pg.sprite.spritecollide(player, enemy_list, True)
        for enemy in collided_enemies:
            player.health -= 25

        collided_coins = pg.sprite.spritecollide(player, coins, True)
        for coin in collided_coins:
            score += 1

        # DRAW SECTION
        screen.fill(BLACK)
        all_sprites.draw(screen)

        health_label = font_health.render("Health: "+str(player.health),True,WHITE)
        score_label = font_score.render("Score: " + str(score),True, WHITE)
        screen.blit(score_label,[100,480])
        screen.blit(health_label,[190,480])

        pg.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
    pg.quit()
    sys.exit()