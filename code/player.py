import pygame 
from settings import *
from support import import_folder
from entity import Entity
import numpy as np
from time import time
from math import pi, cos, sin
import settings

from GUI import Barra_Vida

class Player(Entity):

	
	def __init__(self,pos,groups,obstacle_sprites,create_attack,destroy_attack,create_magic, surface):
		super().__init__(groups)
		self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(-6,HITBOX_OFFSET['player'])

		# graphics setup
		self.import_player_assets()
		self.status = 'down'

		# movement 
		self.attacking = False
		self.attack_cooldown = 400
		self.attack_time = None
		self.obstacle_sprites = obstacle_sprites

		# weapon
		self.create_attack = create_attack
		self.destroy_attack = destroy_attack
		self.weapon_index = 0
		self.weapon = list(weapon_data.keys())[self.weapon_index]
		self.can_switch_weapon = True
		self.weapon_switch_time = None
		self.switch_duration_cooldown = 300

		# magic 
		self.create_magic = create_magic
		self.magic_index = 0
		self.magic = list(magic_data.keys())[self.magic_index]
		self.can_switch_magic = True
		self.magic_switch_time = None

		# stats
		self.stats = {'health': 150,'energy':60,'attack': 10,'magic': 4,'speed': 0.25}
		self.max_stats = {'health': 300, 'energy': 140, 'attack': 20, 'magic' : 10, 'speed': 10}
		self.upgrade_cost = {'health': 100, 'energy': 100, 'attack': 100, 'magic' : 100, 'speed': 100}
		self.health = self.stats['health'] * 0.5
		self.energy = self.stats['energy'] * 0.8
		self.exp = 300
		self.speed = self.stats['speed']

		# damage timer
		self.vulnerable = True
		self.hurt_time = None
		self.invulnerability_duration = 500

		# import a sound
		self.weapon_attack_sound = pygame.mixer.Sound('audio/sword.wav')
		self.weapon_attack_sound.set_volume(0.4)

		#cositas para los mensajes
		self.fondoMensaje = pygame.image.load("graphics/elementos_graficos/fondoMensaje.png")
		self.mess = "" 
		self.tiempoMess = 0
		self.tiempoInicio = 0

		self.wM = 0
		self.fA = 0
		self.hM = 40 
  
		self.barra = Barra_Vida.BarraDeVida(surface)

		

		#cositas para las notas
		self.font = pygame.font.Font(None, 22)		

		self.timeAnt = 0
		self.dt = 0
		self.items_num = [0,0,0,0] 

		#Instrumentos
		self.T_piano = [1,1]


  

	def import_player_assets(self):
		character_path = 'graphics/player/'
		self.animations = {'up': [],'down': [],'left': [],'right': [],
			'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
			'right_attack':[],'left_attack':[],'up_attack':[],'down_attack':[]}

		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)

	def input(self):
		if not self.attacking:
			keys = pygame.key.get_pressed()

			# movement input
			if keys[pygame.K_UP]:
				self.direction.y = -1
				self.status = 'up'
			elif keys[pygame.K_DOWN]:
				self.direction.y = 1
				self.status = 'down'
			else:
				self.direction.y = 0

			if keys[pygame.K_RIGHT]:
				self.direction.x = 1
				self.status = 'right'
			elif keys[pygame.K_LEFT]:
				self.direction.x = -1
				self.status = 'left'
			else:
				self.direction.x = 0

			# attack input 
			if keys[pygame.K_SPACE]:
				self.attacking = True
				self.attack_time = pygame.time.get_ticks()
				self.create_attack()
				self.weapon_attack_sound.play()

			# magic input 
			if keys[pygame.K_LCTRL]:
				self.attacking = True
				self.attack_time = pygame.time.get_ticks()
				style = list(magic_data.keys())[self.magic_index]
				strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
				cost = list(magic_data.values())[self.magic_index]['cost']
				self.create_magic(style,strength,cost)

			"""if keys[pygame.K_q] and self.can_switch_weapon:
				self.can_switch_weapon = False
				self.weapon_switch_time = pygame.time.get_ticks()
				
				if self.weapon_index < len(list(weapon_data.keys())) - 1:
					self.weapon_index += 1
				else:
					self.weapon_index = 0
					
				self.weapon = list(weapon_data.keys())[self.weapon_index]"""

			if keys[pygame.K_e] and self.can_switch_magic:
				self.can_switch_magic = False
				self.magic_switch_time = pygame.time.get_ticks()
				
				if self.magic_index < len(list(magic_data.keys())) - 1:
					self.magic_index += 1
				else:
					self.magic_index = 0

				self.magic = list(magic_data.keys())[self.magic_index]

	def get_status(self):

		# idle status
		if self.direction.x == 0 and self.direction.y == 0:
			if not 'idle' in self.status and not 'attack' in self.status:
				self.status = self.status + '_idle'

		if self.attacking:
			self.direction.x = 0
			self.direction.y = 0
			if not 'attack' in self.status:
				if 'idle' in self.status:
					self.status = self.status.replace('_idle','_attack')
				else:
					self.status = self.status + '_attack'
		else:
			if 'attack' in self.status:
				self.status = self.status.replace('_attack','')
		
		self.barra.Mostrar_vida(self.health,self.stats['health'],self)
		

	def cooldowns(self):
		current_time = pygame.time.get_ticks()

		if self.attacking:
			if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
				self.attacking = False
				self.destroy_attack()

		if not self.can_switch_weapon:
			if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
				self.can_switch_weapon = True

		if not self.can_switch_magic:
			if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
				self.can_switch_magic = True

		if not self.vulnerable:
			if current_time - self.hurt_time >= self.invulnerability_duration:
				self.vulnerable = True

	def animate(self):
		animation = self.animations[self.status]

		# loop over the frame index 
		self.frame_index += self.animation_speed*self.dt
		if self.frame_index >= len(animation):
			self.frame_index = 0

		# set the image
		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)

		# flicker 
		if not self.vulnerable:
			alpha = self.wave_value()
			self.image.set_alpha(alpha)
		else:
			self.image.set_alpha(255)

	def get_full_weapon_damage(self):
		base_damage = self.stats['attack']
		weapon_damage = weapon_data[self.weapon]['damage']
		return base_damage + weapon_damage

	def get_full_magic_damage(self):
		base_damage = self.stats['magic']
		spell_damage = magic_data[self.magic]['strength']
		return base_damage + spell_damage

	def get_value_by_index(self,index):
		return list(self.stats.values())[index]

	def get_cost_by_index(self,index):
		return list(self.upgrade_cost.values())[index]

	def energy_recovery(self):
		if self.energy < self.stats['energy']:
			self.energy += 0.01 * self.stats['magic']
		else:
			self.energy = self.stats['energy'] 

	def printMess(self, mensaje, milisegundos):
		if(self.mess == ""):
			self.mess = mensaje
			self.tiempoInicio = pygame.time.get_ticks()
			self.tiempoMess = milisegundos
		print("funcion PrintMess")

	def deleteMess(self):
		self.mess = ""

	def deleteMessTime(self,milisegundos):
		if self.mess != "":
			self.tiempoMess = milisegundos
			
	def updateMess(self,surface):
		text_surface = self.font.render(self.mess, True, (255, 255, 255))
    
		if pygame.time.get_ticks()-self.tiempoInicio>self.tiempoMess and self.tiempoMess>0:
			self.mess = ""
			text_surface = self.font.render(self.mess, True, (255, 255, 255))
		if self.mess != "":
			esperado = text_surface.get_width()+200
			esperadoFa = 255
		else:
			esperado = 0
			esperadoFa = 0
            
		dif = esperado-self.wM
		self.wM +=dif*0.2

		dif = esperadoFa-self.fA
		self.fA+=dif*0.2
		
		fondoMensajeMod = pygame.transform.scale(self.fondoMensaje, (int(self.wM), int(self.hM)))
		surface.blit(fondoMensajeMod, (settings.SCREEN_WIDTH/2-self.wM//2,20))
		
		text_x = settings.SCREEN_WIDTH/2 - text_surface.get_width()/2
		text_y = 33

		text_surface.set_alpha(self.fA)

		surface.blit(text_surface, (text_x, text_y))
	
	def get_center(self):
		return self.rect.center

	def update(self):
		self.input()
		self.cooldowns()
		self.get_status()
		self.animate()
		self.move(self.stats['speed']*self.dt)
		self.energy_recovery()
		self.dt = (pygame.time.get_ticks()-self.timeAnt)
		self.timeAnt = pygame.time.get_ticks()
	
