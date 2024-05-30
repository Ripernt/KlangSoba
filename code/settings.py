import pygame

SCREEN_WIDTH    = 1280	
SCREEN_HEIGHT   = 720
FPS      = 60
TILESIZE = 64


BLACK    = (   0,   0,   0) 
WHITE    = ( 255, 255, 255) 
BLUE     = (   0,   0, 255)

HITBOX_OFFSET = {
	'player': -26,
	'object': -40,
	'grass': -10,
	'invisible': 0}

# ui 
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = 'graphics/font/joystix.ttf'
UI_FONT_SIZE = 18


WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'


TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'

botonBlue = pygame.image.load("graphics/elementos_graficos/bluebut.png")
botonBlue = pygame.transform.scale(botonBlue, (180, 100))

botonRed = pygame.image.load("graphics/elementos_graficos/redbut.png")
botonRed = pygame.transform.scale(botonRed, (180, 100))

botonPur = pygame.image.load("graphics/elementos_graficos/purbut.png")
botonPur = pygame.transform.scale(botonPur, (180, 100))

botonPurChat = pygame.image.load("graphics/elementos_graficos/purbut.png")
botonPurChat = pygame.transform.scale(botonPur, (80, 80))

botonGreen = pygame.image.load("graphics/elementos_graficos/greenbut.png")
botonGreen = pygame.transform.scale(botonGreen, (180, 100))

botonPiano = pygame.image.load("graphics/elementos_graficos/Piano.png")
botonPiano = pygame.transform.scale(botonPiano, (200, 200))

#botonTPiano = pygame.image.load("graphics/elementos_graficos/purbut.png")
#botonTPiano = pygame.transform.scale(botonTPiano, (50,50))


#Botones del piano
botonREPiano = pygame.image.load("graphics/elementos_graficos/re.png")
botonREPiano = pygame.transform.scale(botonREPiano, (60,200))
botonTECLAPiano = pygame.image.load("graphics/elementos_graficos/tecla.png")
botonTECLAPiano = pygame.transform.scale(botonTECLAPiano, (60,200))
botonDOPiano = pygame.image.load("graphics/elementos_graficos/do.png")
botonDOPiano = pygame.transform.scale(botonDOPiano, (60,200))
botonMIPiano = pygame.image.load("graphics/elementos_graficos/mi.png")
botonMIPiano = pygame.transform.scale(botonMIPiano, (60,200))
botonNEGRAPiano = pygame.image.load("graphics/elementos_graficos/negra.png")
botonNEGRAPiano = pygame.transform.scale(botonNEGRAPiano, (18,102))


#Boton para grabar
botonGrabar = pygame.image.load("graphics/elementos_graficos/rec_start.png")
botonGrabar = pygame.transform.scale(botonGrabar, (50,50))

#Boton para dejar de grabar
botonStopGrabar = pygame.image.load("graphics/elementos_graficos/rec_stop.png")
botonStopGrabar = pygame.transform.scale(botonStopGrabar, (50,50))

#Boton para guardar pista
botonGuardarPista = pygame.image.load("graphics/elementos_graficos/save.png")
botonGuardarPista = pygame.transform.scale(botonGuardarPista, (50,50))

#Boton grabando
botonGrabando = pygame.image.load("graphics/elementos_graficos/recording.png")
botonGrabando = pygame.transform.scale(botonGrabando, (50,50))

#Boton no grabando
botonNoGrabando = pygame.image.load("graphics/elementos_graficos/notRecording.png")
botonNoGrabando = pygame.transform.scale(botonNoGrabando, (50,50))

#Boton sintetizador
botonSintetizador = pygame.image.load("graphics/elementos_graficos/Sintetizador.png")
botonSintetizador = pygame.transform.scale(botonSintetizador,(200, 200))

#Botones de instrumentos bloqueados
botonSintetizadorBloqueado = pygame.image.load("graphics/elementos_graficos/sintetizadorBloqueado.png")
botonSintetizadorBloqueado = pygame.transform.scale(botonSintetizadorBloqueado,(200,200))
botonPianoBloqueado = pygame.image.load("graphics/elementos_graficos/pianoBloqueado.png")
botonPianoBloqueado = pygame.transform.scale(botonPianoBloqueado,(200,200))

botonMezcladora = pygame.image.load("graphics/elementos_graficos/purbut.png")
botonMezcladora = pygame.transform.scale(botonMezcladora,(200,200))

generalButton=pygame.image.load("graphics/elementos_graficos/botonkS.png")
generalButton=pygame.transform.scale(generalButton,(240,90))

botonRegresar = pygame.image.load("graphics/elementos_graficos/botonT.png")
botonRegresar = pygame.transform.scale(botonRegresar,(50,50))

botonBorrarGrabacion = pygame.image.load("graphics/elementos_graficos/trash.png")
botonBorrarGrabacion = pygame.transform.scale(botonBorrarGrabacion,(50,50))

botonArchivoMusica = pygame.image.load("graphics/elementos_graficos/foldermusica.png")
botonArchivoMusica = pygame.transform.scale(botonArchivoMusica,(50,50))

botonSoporte = pygame.image.load("graphics/elementos_graficos/soporte.png")
botonSoporte = pygame.transform.scale(botonSoporte, (50,50))

botonPausar = pygame.image.load("graphics/elementos_graficos/pausaboton.png")
botonPausar = pygame.transform.scale(botonPausar, (50,50))

weapon_data = {
	'sword': {'cooldown': 100, 'damage': 15,'graphic':'graphics/weapons/sword/full.png'},
	'lance': {'cooldown': 400, 'damage': 30,'graphic':'graphics/weapons/lance/full.png'},
	'axe': {'cooldown': 300, 'damage': 20, 'graphic':'graphics/weapons/axe/full.png'},
	'rapier':{'cooldown': 50, 'damage': 8, 'graphic':'graphics/weapons/rapier/full.png'},
	'sai':{'cooldown': 80, 'damage': 10, 'graphic':'graphics/weapons/sai/full.png'}}

magic_data = {
	'flame': {'strength': 5,'cost': 20,'graphic':'graphics/particles/flame/fire.png'},
	'heal' : {'strength': 20,'cost': 10,'graphic':'graphics/particles/heal/heal.png'},
    'ray': {'strength': 5,'cost': 20,'graphic':'graphics/particles/ray/rayo.png'},
    'magic': {'strength': 5,'cost': 20,'graphic':'graphics/particles/magic/magico.png'}}

monster_data = {
	'squid': {'health': 100,'exp':100,'damage':10,'attack_type': 'slash', 'attack_sound':'audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
	'raccoon': {'health': 400,'exp':300,'damage':50,'attack_type': 'claw',  'attack_sound':'audio/attack/claw.wav','speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
	'spirit': {'health': 100,'exp':90,'damage':8,'attack_type': 'thunder', 'attack_sound':'audio/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
	'bamboo': {'health': 70,'exp':80,'damage':6,'attack_type': 'leaf_attack', 'attack_sound':'audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300}}


logros_data = {
	"B1": {"nombre": "Una Nueva aventura", "descripcion": "KS a iniciado"},
    "B2": {"nombre": "Haz terminado con una creatura", "descripcion": "Gana el juego"},
    "B3": {"nombre": "MUERTE", "descripcion": "Volveras mas fuerte"},
    "B4": {"nombre": "Zurdo", "descripcion": "haz caminado a la izquierda"},
    "B5": {"nombre": "Duro de matar", "descripcion": "haz matado a 20 enemigos"},
    "B6": {"nombre": "MUERTE", "descripcion": "Volveras mas fuerte"},
    
	}

npc_data = {
    'mixer':{'notice_radius' : 150},
    'jesus':{}
}