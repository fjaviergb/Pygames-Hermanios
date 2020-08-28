#####################################
# VARIABLES DE CARACTERIZACION
#####################################
WIDTH = 500
HEIGHT = 500
HALF_SCREEN_X = WIDTH / 2  # Posicion media del eje X
HALF_SCREEN_Y = HEIGHT / 2 # Posicion media del eje Y
LIVEINIT = 10  # Cantidad de vida
DIS_SECURE = 2  # Dis en dis_tic de seguridad para no entrar
DISMAX_TIC = 8  # Dis maxima por tick en el dasheo
APT_SWORD = 3  # Angle per tick, de la espada. Empleado everywhere
DISMAX = 80  # Dis máxima que se realiza en el dasheo
ENERGYMAX = 100  # Energía completa
EPT_RUN = 2  # Energy per tic consumido al correr
EPT_RECOVER = 1  # Energy per tic recuperado
APT_SWORD_SWINGLIMIT = 30  # Este parámetro, junto a apt_sword,
# determina el angulo que alcanza al cargar. En sword_collision().
# Angulo que gira = 30 * 3 = 90
APT_SWORD_SLASHLIMIT = -20  # Este parámtro, junto a apt_sword.
# determina el ángulo que alcanza en el sentido contrario del swing.
# En sword_collision(). Angulo que gira = -20 * 3 = -60
APT_SWORD_CLASHLIMIT = 20  # Este parámtro, junto a apt_sword.
# determina el ángulo que alcanza en el sentido del swing, al colisionar..
# En sword_collision().
DASH_CD = 5000  # Cooldown, en milisegundos, para el dash.
VELOCITY = 2
IPT_CHARGECOUNT_SLASH = 5 #Incremento del chargecount sin colisión en función sword_collision
IPT_CHARGECOUNT_STANDARD = 1 #Incremento del chargecount sin colision en funcion sword_movement


BODY_RADIO = 20
BODY_IMG_WIDTH = 50
BODY_IMG_HEIGHT = 50

HAND_RADIO = 10
HAND_IMG_WIDTH = 50
HAND_IMG_HEIGHT = 50

SWORD_WIDTH = 5
SWORD_HEIGHT = 50
SWORD_IMG_WIDTH = 50
SWORD_IMG_HEIGHT = 120

LIVEBAR_WIDTH = 100
LIVEBAR_HEIGHT = 5
LIVEBAR_TOPLEFT_X = 50
LIVEBAR_TOPLEFT_Y = 490

ENERGYBAR_WIDTH = 100
ENERGYBAR_HEIGHT = 5
ENERGYBAR_TOPLEFT_X = 50
ENERGYBAR_TOPLEFT_Y =  480
ENERGYBAR_BLACK_BORDER = 2 # Indica el pixel que actua de borde negro