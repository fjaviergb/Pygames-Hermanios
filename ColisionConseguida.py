import pygame
import pandas as pd
import math
pygame.init()

class init(object):
     def __init__(self,width,height):
         self.width = width
         self.height = height
         self.image = pygame.Surface((width,height))
         self.image.fill((0,0,0))
         self.clocktime = pygame.time.Clock()
         self.run = True
         self.name = 'GAME 1'

     def draw(self,win):
        win.blit(self.image, (0,0))

class char(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        self.image = pygame.Surface((width,height))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.topleft = (self.x,self.y)
        self.vel = 2
        self.xaxis = 0
        self.yaxis = 0
        
    def draw(self,win):
        win.blit(self.image, (self.rect.x,self.rect.y))
            
    def collision_with(self, obstacle):
        self.rect.x += self.vel * self.xaxis
        if self.rect.colliderect(obstacle.rect):
            if self.xaxis > 0:
                self.rect.right = obstacle.rect.left
                self.x = self.rect.x
            else:
                self.rect.left = obstacle.rect.right
# =============================================================================
#             import pdb
#             pdb.set_trace()
# =============================================================================
        self.rect.y += self.vel * self.yaxis
        if self.rect.colliderect(obstacle.rect):
            if self.yaxis > 0:
                self.rect.bottom = obstacle.rect.top
            else:
                self.rect.top = obstacle.rect.bottom

init = init(500,500)
player = char(250,250,50,50)
environment = char(100,100,100,100)
win = pygame.display.set_mode((init.width,init.height))
pygame.display.set_caption(init.name)

def redraw(win):
    init.draw(win)
    environment.draw(win)
    player.draw(win)
    pygame.display.update()

while init.run:
    init.clocktime.tick(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            init.run = False
   
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: 
                    player.xaxis = -1
        
            if event.key == pygame.K_RIGHT: 
                    player.xaxis = 1
                    
            if event.key == pygame.K_UP: 
                    player.yaxis = -1
                    
            if event.key == pygame.K_DOWN: 
                    player.yaxis = 1
                    
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player.xaxis < 0: 
                    player.xaxis = 0
        
            if event.key == pygame.K_RIGHT and player.xaxis > 0: 
                    player.xaxis = 0
                    
            if event.key == pygame.K_UP and player.yaxis < 0: 
                    player.yaxis = 0
                    
            if event.key == pygame.K_DOWN  and player.yaxis > 0: 
                    player.yaxis = 0
            
    player.collision_with(environment)
    
    redraw(win)

pygame.quit()



