import pygame as pg

def is_swinging(self):
    return self.swingleft or self.swingright or self.slashleft or self.slashright or self.backleft or self.backright


def sword_movement(self, swing, angle_hit_orientation, button_click, slash, quadrant_angle, back, angle_grad, clash):
    if getattr(self, swing):
        if self.chargecount <= self.apt_sword_swinglimit:
            self.anglehit = self.angle + self.chargecount * angle_hit_orientation * self.apt_sword
            self.chargecount += 1
        if button_click == 0:
            self.countlimit = self.chargecount
            setattr(self, slash, True)
            setattr(self, swing, False)
        else:
            self.anglehit = self.angle + self.chargecount * angle_hit_orientation * self.apt_sword
    elif getattr(self, slash) and not getattr(self, swing) and not getattr(self, back):
        if self.chargecount >= self.countlimit * self.apt_sword_slashlimit / self.apt_sword_swinglimit:
            self.sword_collision(angle_grad, angle_hit_orientation, quadrant_angle, self.chargecount)
        else:
            setattr(self, slash, False)
            setattr(self, back, True)
    elif getattr(self, back):
        if self.chargecount <= 1:
            self.anglehit = self.angle + self.chargecount * angle_hit_orientation * self.apt_sword
            self.chargecount += 1
        else:
            setattr(self, back, False)
            self.chargecount = 1
    elif getattr(self, clash):
        if self.chargecount <= self.clash_count + self.apt_sword_clashlimit:
            self.anglehit = self.angle + self.chargecount * angle_hit_orientation * self.apt_sword
            self.chargecount += 1
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
