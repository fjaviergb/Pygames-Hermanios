import pygame

class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x,y,width,height)
        self.vel = 3

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.x += self.vel

        if keys[pygame.K_UP]:
            self.y -= self.vel

        if keys[pygame.K_DOWN]:
            self.y += self.vel

        self.rect = (self.x, self.y, self.width, self.height)
        
class hand():
    def __init__(self, ori):
        self.radio = 10
        self.handspeed = 1
        self.ori = ori
        self.image = pygame.Surface((50,50))
        self.image.set_colorkey((0,0,0))
        self.x = 0
        self.y = 0
        self.vel = 3
        
        if ori == 1:
            pygame.draw.circle(self.image, ((255,0,0)), (10,10), self.radio)
            self.rect = self.image.get_rect(topleft = (0,0))
        else:
           pygame.draw.circle(self.image, ((0,255,0)), (40,10), self.radio)
           self.rect = self.image.get_rect(topleft = (0,0))

    def update(self):           
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.x += self.vel

        if keys[pygame.K_UP]:
            self.y -= self.vel

        if keys[pygame.K_DOWN]:
            self.y += self.vel

        self.rect.topleft = (self.x, self.y)
        
        