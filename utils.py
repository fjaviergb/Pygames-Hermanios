import pygame as pg
from variables import *

def is_swinging(self):
    return self.swingleft or self.swingright or self.slashleft or self.slashright or self.backleft or self.backright or self.clashright or self.clashleft

def sword_movement(self, swing, angle_hit_orientation, button_click, slash, quadrant_angle, back, angle_grad, clash):
    if getattr(self, swing):
        if self.chargecount <= APT_SWORD_SWINGLIMIT:
            self.anglehit = self.angle + self.chargecount * angle_hit_orientation * APT_SWORD
            self.chargecount += IPT_CHARGECOUNT_STANDARD
        if button_click == 0:
            self.countlimit = self.chargecount
            setattr(self, slash, True)
            setattr(self, swing, False)
        else:
            self.anglehit = self.angle + self.chargecount * angle_hit_orientation * APT_SWORD
    elif getattr(self, slash) and not getattr(self, swing) and not getattr(self, back):
        if self.chargecount >= self.countlimit * APT_SWORD_SLASHLIMIT / APT_SWORD_SWINGLIMIT:
            self.sword_collision(angle_grad, angle_hit_orientation, quadrant_angle, self.chargecount)
        else:
            setattr(self, slash, False)
            setattr(self, back, True)
    elif getattr(self, back):
        if self.chargecount <= 1:
            self.anglehit = self.angle + self.chargecount * angle_hit_orientation * APT_SWORD
            self.chargecount += IPT_CHARGECOUNT_STANDARD
        else:
            setattr(self, back, False)
            self.chargecount = 1
    elif getattr(self, clash):
        if self.chargecount <= self.clash_count + APT_SWORD_CLASHLIMIT:
            self.anglehit = self.angle + self.chargecount * angle_hit_orientation * APT_SWORD
            self.chargecount += IPT_CHARGECOUNT_STANDARD
        else:
            self.clash_count = 0
            self.chargecount = 1
            setattr(self, clash, False)

def sprite_collision(self, sprite, group):
    if sprite:
        block_hit_list = pg.sprite.spritecollide(getattr(self,sprite), getattr(self,group), False)
        block_hit_list_masked = pg.sprite.spritecollide(
            getattr(self,sprite), block_hit_list, False, pg.sprite.collide_mask
        )
    else:
        block_hit_list = pg.sprite.spritecollide(self, getattr(self,group), False)
        block_hit_list_masked = pg.sprite.spritecollide(
            self, block_hit_list, False, pg.sprite.collide_mask
        )
    return block_hit_list_masked
