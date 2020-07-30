import pygame as pg
from SuperPlayer import body

pg.init()
# OBLIGATORIO

screen_size = (500, 500)
# Tamaño de la pantalla en pixels. Necesario Tupla

bg = pg.display.set_mode(screen_size)
# Clase de tipo 'Surface' que se establece como display
# Una 'surface' es un rectángulo de pixels delimitado; en este caso 500x500
# El color predeterminado de las 'surfaces' es el negro (0,0,0)

pg.display.set_caption("Cuerpo Básico")
# Nombre que se le asigna al display

WHITE = (255, 255, 255)

p = body(250, 250)
all_sprites = pg.sprite.Group()
all_sprites.add(p)
all_sprites.add(p.rightH)
all_sprites.add(p.leftH)
all_sprites.add(p.espada)
all_sprites.add(p.energybar)

clock = pg.time.Clock()
run = True
while run:
    clock.tick(60)
    # Repite el bucle el número de veces que le pasas como argumento por segundo
    # Son los FPS (Frames per second)

    for event in pg.event.get():
        # Itera entre todos los eventos que pueden suceder durante el bucle
        # Se deben diferenciar entre TYPES y otros atributos más específicos
        # Ejemplo:
        # >> event.type == pg.QUIT
        # >> event.type == pg.KEYDOWN (evento que se dispara cuando se pulsa una tecla)
        # >> event.type == pg.KEYUP (evento que se dispara cuando se pulsa una tecla)
        # >> event.key = pg.K_LEFT (evento que se dispara cuando se pulsa la tecla LEFT)

        if event.type == pg.QUIT:
            run = False

    bg.fill(WHITE)
    # La 'surface' que llama al método se colorea enteramente de blanco

    all_sprites.update(p)
    all_sprites.draw(bg)
    pg.display.update()
    # Actualiza todas las 'Surfaces' en el display llamando al método update()

pg.quit()
# OBLIGATORIO
