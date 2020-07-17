import pygame as pg
from network import Network
from SuperPlayer import body
from otherplayer import otherbody
import otherenvironment as env

width = 500
height = 500
win = pg.display.set_mode((width, height))
pg.display.set_caption("Client")

def colision(p, sword):
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

        pothers = n.send((p.tipo,p.x,p.y,p.angle,p.anglehit,p.slashright,p.slashleft, p.live, p.chargecount))

        win.fill((255,255,255))
        
        for i in pothers:        
            if type(i) != list:
                if (p.x,p.y) != (i[1],i[2]) and i[7] > 0:
                    po = otherbody(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8])
    
                    p.other_sprites.add(po)
                    p.other_sprites.add(po.Rhand)
                    p.other_sprites.add(po.Lhand)
                    p.other_sprites.add(po.espada) 
                    p.other_sprites.update(po)
                    p.other_sprites.draw(win)
                    p.enem_sword.add(po.espada)
    
                    p.col_sprites.add(po)                
    
                    if i[8] == 31 or i[6] or i[5]:
                        p.col_sprites.add(po.espada)                
                    
                    if i[5] or i[6]:
                        block_hit_list = pg.sprite.spritecollide(p, p.enem_sword, False)
                        block_hit_list_masked = pg.sprite.spritecollide(p, block_hit_list, False, pg.sprite.collide_mask)
                        if len(block_hit_list_masked) != 0:
                            p.live -= 1
                        p.enem_sword = pg.sprite.Group()
                    
                    colision(p, p.espada)
    
                    p.other_sprites = pg.sprite.Group()   
        
            else:
                for j in i:
                    if j[0] == 4:
                        envir = env.circle_obstacle(j[1],j[2])   
                        p.env_sprites.add(envir)
                    elif j[0] == 3:
                        envir = env.rect_obstacle(j[1],j[2])   
                        p.env_sprites.add(envir)
                    elif j[0] == 2: 
                        envir = env.gir_obstacle(j[1],j[2])   
                        p.env_sprites.add(envir)
        
                    p.env_sprites.update()
                    p.env_sprites.draw(win)
                    p.col_sprites.add(envir)                
                    
                    colision(p, p.espada)

                p.env_sprites = pg.sprite.Group()
        
        if p.live > 0:           
            all_sprites.update(p)
            p.col_sprites = pg.sprite.Group()  
            p.enem_sword = pg.sprite.Group()                          
            all_sprites.draw(win)

        pg.display.update()

main()