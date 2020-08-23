def is_swinging(self):
    return self.swingleft or self.swingright or self.slashleft or self.slashright or self.backleft or self.backright


def sword_movement(self, swing, angle_hit_orientation, button_click, slash, quadrant_angle, back, angle_grad, clash):
    if getattr(self, swing):
        if self.chargecount <= 30:
            self.anglehit = self.angle + self.chargecount * 3 * angle_hit_orientation
            self.chargecount += 1
        if button_click == 0:
            self.countlimit = self.chargecount
            setattr(self, slash, True)
            setattr(self, swing, False)
        else:
            self.anglehit = self.angle + self.chargecount * 3 * angle_hit_orientation
    elif getattr(self, slash) and not getattr(self, swing) and not getattr(self, back):
        if self.chargecount >= self.countlimit * -20 / 30:
            self.sword_collision(angle_grad, angle_hit_orientation, quadrant_angle, self.chargecount)
        else:
            setattr(self, slash, False)
            setattr(self, back, True)
    elif getattr(self, back):
        if self.chargecount <= 1:
            self.anglehit = self.angle + self.chargecount * 3 * angle_hit_orientation
            self.chargecount += 1
        else:
            setattr(self, back, False)
            self.chargecount = 1
    elif getattr(self, clash):
        if self.chargecount <= self.clash_count + 20:
            self.anglehit = self.angle + self.chargecount * 3 * angle_hit_orientation
            self.chargecount += 1
        else:
            self.clash_count = 0
            self.chargecount = 1
            setattr(self, clash, False)
