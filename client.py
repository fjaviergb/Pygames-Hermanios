import pygame
from network import Network
from player2 import Player, hand

width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


def redrawWindow(win, pothers):
    win.fill((255,255,255))
    for p in pothers:
        for i in p:
            i.draw(win)
    pygame.display.update()


def main():
    run = True
    p = Player(0,0,50,50,(255,0,0))
    h = hand(0)
    all_sprites = (p,h)
    n = Network()
    
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                n.send(False)  
                n.client.close()
                run = False
                pygame.quit()

        for i in all_sprites:
            i.update()
        pothers = n.send(all_sprites)        
        redrawWindow(win, pothers)

main()