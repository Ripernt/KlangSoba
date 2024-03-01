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
botonBlue = pygame.transform.scale(botonBlue, (180, 180))

botonRed = pygame.image.load("graphics/elementos_graficos/redbut.png")
botonRed = pygame.transform.scale(botonRed, (180, 180))

botonPur = pygame.image.load("graphics/elementos_graficos/purbut.png")
botonPur = pygame.transform.scale(botonPur, (180, 180))

botonPurChat = pygame.image.load("graphics/elementos_graficos/purbut.png")
botonPurChat = pygame.transform.scale(botonPur, (80, 80))

botonGreen = pygame.image.load("graphics/elementos_graficos/greenbut.png")
botonGreen = pygame.transform.scale(botonGreen, (180, 180))

generalButton=pygame.image.load("graphics/elementos_graficos/botonkS.png")
generalButton=pygame.transform.scale(generalButton,(240,90))


weapon_data = {
	'sword': {'cooldown': 100, 'damage': 15,'graphic':'graphics/weapons/sword/full.png'},
	'lance': {'cooldown': 400, 'damage': 30,'graphic':'graphics/weapons/lance/full.png'},
	'axe': {'cooldown': 300, 'damage': 20, 'graphic':'graphics/weapons/axe/full.png'},
	'rapier':{'cooldown': 50, 'damage': 8, 'graphic':'graphics/weapons/rapier/full.png'},
	'sai':{'cooldown': 80, 'damage': 10, 'graphic':'graphics/weapons/sai/full.png'}}

magic_data = {
	'flame': {'strength': 5,'cost': 20,'graphic':'graphics/particles/flame/fire.png'},
	'heal' : {'strength': 20,'cost': 10,'graphic':'graphics/particles/heal/heal.png'}}

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