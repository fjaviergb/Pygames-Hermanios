import pygame as pg
from network import Network
from SuperPlayer import body
from otherplayer import otherbody

width = 500
height = 500
win = pg.display.set_mode((width, height))
pg.display.set_caption("Client")

def colision(p, sword, po):
    if ((p.slashleft and not p.swingleft and not p.backleft) or (p.slashright and not p.swingright and not p.backright) or (p.chargecount == 31 and p.swingleft)):
        block_hit_list = pg.sprite.spritecollide(sword, p.col_sprites, False)
        block_hit_list_masked = pg.sprite.spritecollide(sword, block_hit_list, False, pg.sprite.collide_mask)
        for block in block_hit_list_masked:
            if p.slashleft:
                p.clashleft = True
                p.clash_count = p.chargecount                    
                p.slashleft = False                
                p.backleft = False
                p.slashright = False                
                p.backright = False
                p.swingleft = False
                p.swingright = False
            elif p.slashright:
                p.clashright = True
                p.clash_count = p.chargecount
                p.slashleft = False                
                p.backleft = False
                p.slashright = False                
                p.backright = False
                p.swingleft = False
                p.swingright = False

def main():
    run = True
    p = body()
    all_sprites = pg.sprite.Group()
    
    all_sprites.add(p)
    all_sprites.add(p.rightH)
    all_sprites.add(p.leftH)
    all_sprites.add(p.espada)
    n = Network()
    
    clock = pg.time.Clock()

    while run:
        clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                n.send(False)  
                n.client.close()
                run = False
                pg.quit()

        pothers = n.send((p.x,p.y,p.angle,p.anglehit,p.slashright,p.slashleft, p.live, p.chargecount))
            
        win.fill((255,255,255))
        
        for i in pothers:        
            if (p.x,p.y) != (i[0],i[1]) and i[6] > 0:
                po = otherbody(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7])

                p.other_sprites.add(po)
                p.other_sprites.add(po.Rhand)
                p.other_sprites.add(po.Lhand)
                p.other_sprites.add(po.espada) 
                p.other_sprites.update(po)
                p.other_sprites.draw(win)
                p.enem_sword.add(po.espada)

                p.col_sprites.add(po)                

                if i[7] == 31 and i[5] and i[4]:
                    p.col_sprites.add(po.espada)                
                
                if i[4] or i[5]:
                    block_hit_list = pg.sprite.spritecollide(p, p.enem_sword, False)
                    block_hit_list_masked = pg.sprite.spritecollide(p, block_hit_list, False, pg.sprite.collide_mask)
                    if len(block_hit_list_masked) != 0:
                        p.live -= 1
                    p.enem_sword = pg.sprite.Group()
                
                colision(p, p.espada, po)

                p.other_sprites = pg.sprite.Group()   
        
        if p.live > 0:           
            all_sprites.update(p)
            p.col_sprites = pg.sprite.Group()  
            p.enem_sword = pg.sprite.Group()                          
            all_sprites.draw(win)

        pg.display.update()

main()