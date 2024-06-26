import pygame, time
from settings import *
from entity import Entity
from support import *
from ui import UI
from logros import Logros
from GUI.Barra_Vida import BarraDeVida
from GUI.MenuMezcladora import *
from item import Item
from player import Player
from pygame.locals import *


class NPC(Entity):

	def __init__(self,npc_name,pos,groups,obstacle_sprites,surface):

		super().__init__(groups)
		self.sprite_type = 'npc'
		self.status = 'idle'
		# cositas de los graficos
		self.import_graphics(npc_name)
		self.status = 'idle'
		#sprite del npc
		self.image = self.animations[self.status][self.frame_index]
		
		# movimiento
		self.rect = self.image.get_rect(topleft = pos) 
		self.hitbox = self.rect.inflate(0,-10)
		self.obstacle_sprites = obstacle_sprites

		#estadisticas
		self.npc_name = npc_name
		npc_info = npc_data[self.npc_name]
		self.notice_radius = npc_info['notice_radius']

		self.display_surface = surface
		#self.logros = Logros(self.display_surface)
  
		self.timeAnt = 0
		self.dt = 0

		self.conexion = None
		self.cursor = None
		self.screen = None

	def import_graphics(self,name):
		self.animations = {'idle':[]}
		main_path = f'graphics/npcs/{name}/'
		for animation in self.animations.keys():
			self.animations[animation] = import_folder(main_path + animation)

	def get_player_distance_direction(self,player):
		enemy_vec = pygame.math.Vector2(self.rect.center)
		player_vec = pygame.math.Vector2(player.rect.center)
		distance = (player_vec - enemy_vec).magnitude()

		if distance > 0:
			direction = (player_vec - enemy_vec).normalize()
		else:
			direction = pygame.math.Vector2()

		return (distance,direction)

	def animate(self):
		animation = self.animations[self.status]
		
		self.frame_index += self.animation_speed*self.dt
		if self.frame_index >= len(animation):
			if self.status == 'attack':
				self.can_attack = False
			self.frame_index = 0

		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)

	def mostrar_caja_dialogo(surface, x, y, width, height, text):
		font = pygame.font.Font('graphics/font/joystix.ttf', 20)
		pygame.draw.rect(surface, BLACK, (x, y, width, height))
		pygame.draw.rect(surface, WHITE, (x, y, width, height), 2)
		text_x = x + 10
		text_y = y + 10
		for char in text:
			text_surface = font.render(char, True, WHITE)
			surface.blit(text_surface, (text_x, text_y))
			text_x += text_surface.get_width()
			pygame.display.flip()
			pygame.time.delay(50)
		return pygame.time.get_ticks()
			

	def get_status(self, player):
		
		distance = self.get_player_distance_direction(player)[0]

		if distance <= self.notice_radius:

			if self.npc_name == 'jimmy':
				self.mandar_npc(self.npc_name)
			else:
				pass
			if self.npc_name == 'jesus':
				self.mandar_npc(self.npc_name)
			else:
				pass
			if self.npc_name == 'bernabe':	
				self.mandar_npc(self.npc_name)
			else:
				pass
			if self.npc_name == 'mixer':
				self.mandar_npc(self.npc_name)
			else:
				pass


	def mandar_npc(self,nombre_npc):
		global npc
		self.npc_temporal = nombre_npc
		npc = self.npc_temporal
	
	def obtener_npc():
		return npc
	def update(self):
		
		self.animate()
		self.dt = (pygame.time.get_ticks()-self.timeAnt)
		self.timeAnt = pygame.time.get_ticks()

	def npc_update(self,player):
		self.get_status(player)