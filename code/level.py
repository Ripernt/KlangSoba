import threading, time, pygame, random
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice, randint
from weapon import Weapon
from ui import UI

from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade
from GUI.Barra_Vida import BarraDeVida
from logros import Logros
from item import Item


class Level:
	def __init__(self, n=1, mapa="ground", scale=1, player=None):
		
		 
		self.display_surface = pygame.display.get_surface()
		self.game_paused = False
		
		self.visible_sprites = YSortCameraGroup(mapa, scale)
		self.obstacle_sprites = pygame.sprite.Group()

		# attack sprites
		self.current_attack = None
		self.attack_sprites = pygame.sprite.Group()
		self.attackable_sprites = pygame.sprite.Group()
		self.capasCargadas = 0
  
		self.player = player
		self.posInit = (0,0)
 
 		
 
		# sprite setup
		self.create_map(n)

		print(self.capasCargadas)
		while(self.capasCargadas<4):
			print("esperando a que carguen las capas...")
			print(self.capasCargadas)
			time.sleep(1)
		time.sleep(2)
		# user interface 
		self.ui = UI(Player=self.player)
		self.upgrade = Upgrade(self.player)
		
		# particles
		self.animation_player = AnimationPlayer()
		self.magic_player = MagicPlayer(self.animation_player)

  
	def cargarCSV(self, style, layout, graphics):
		from enemy import Enemy
		from Npc import NPC

		for row_index,row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != '-1':
						x = col_index * TILESIZE
						y = row_index * TILESIZE
						if style == 'boundary':
							Tile((x,y),[self.obstacle_sprites],'invisible')
						if style == 'grass':
							random_grass_image = choice(graphics['grass'])
							Tile(
								(x,y),
								[self.visible_sprites,self.obstacle_sprites,self.attackable_sprites],
								'grass',
								random_grass_image)

						if style == 'object':
							surf = graphics['objects'][int(col)]
							Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'object',surf)

						if style == 'entities':
							if col == '394':
								if(self.player==None):
									self.posInit = (x,y)
									self.player = Player(
										(x,y),
										[self.visible_sprites],
										self.obstacle_sprites,
										self.create_attack,
										self.destroy_attack,
										self.create_magic, 
										self.display_surface)
								else:
									
									self.posInit = (x,y)
									print("esta es la posicion inicial: ", self.posInit)
								
							else:
								if col == '390': 
									monster_name = 'bamboo'
									Enemy(
										monster_name,
										(x,y),
										[self.visible_sprites,self.attackable_sprites],
										self.obstacle_sprites,
										self.damage_player,
										self.trigger_death_particles,
										self.add_exp,
										self.drop_item, self.display_surface)	
								elif col == '391': 
									monster_name = 'spirit'
									Enemy(
										monster_name,
										(x,y),
										[self.visible_sprites,self.attackable_sprites],
										self.obstacle_sprites,
										self.damage_player,
										self.trigger_death_particles,
										self.add_exp,
										self.drop_item, self.display_surface)
								elif col == '392': 
									monster_name ='raccoon'
									Enemy(
										monster_name,
										(x,y),
										[self.visible_sprites,self.attackable_sprites],
										self.obstacle_sprites,
										self.damage_player,
										self.trigger_death_particles,
										self.add_exp,
										self.drop_item, self.display_surface)
								elif col == '397': 
									npc_name = 'mixer'
									NPC(
										npc_name,
										(x,y),
										[self.visible_sprites],
										self.obstacle_sprites,
										self.display_surface,	
									)
								elif col == '398': 
									npc_name = 'jesus'
									NPC(
										npc_name,
										(x,y),
										[self.visible_sprites],
										self.obstacle_sprites,
										self.display_surface,	
									)
								elif col == '399':
									npc_name = 'bernabe'
									NPC(
										npc_name,
										(x,y),
										[self.visible_sprites],
										self.obstacle_sprites,
										self.display_surface,	
									)
								elif col == '400':
									npc_name = 'jimmy'
									NPC(
										npc_name,
										(x,y),
										[self.visible_sprites],
										self.obstacle_sprites,
										self.display_surface,	
									)									
								else: 
									monster_name = 'squid'
									Enemy(
										monster_name,
										(x,y),
										[self.visible_sprites,self.attackable_sprites],
										self.obstacle_sprites,
										self.damage_player,
										self.trigger_death_particles,
										self.add_exp,
										self.drop_item, self.display_surface)
						
		self.capasCargadas+=1
		print(style)

	def create_map(self, num):
		
		layouts = {
			'boundary': import_csv_layout(f'map/{num}/map_FloorBlocks.csv'),
			'grass': import_csv_layout(f'map/{num}/map_Grass.csv'),
			'object': import_csv_layout(f'map/{num}/map_Objects.csv'),
			'entities': import_csv_layout(f'map/{num}/map_Entities.csv')
		}
		graphics = {
			'grass': import_folder('graphics/Grass'),
			'objects': import_folder('graphics/objects')
		}

		for style,layout in layouts.items():
			threadLevel = threading.Thread(target=self.cargarCSV, args=(style, layout, graphics))
			threadLevel.start()
            

		print("se ha creado el mapa")					
	def resetPlayer(self):
		self.player.kill()
		self.player.add([self.visible_sprites])
		
		"""self.obstacle_sprites,
										self.create_attack,
										self.destroy_attack,
										self.create_magic, 
										self.display_surface"""
		self.player.obstacle_sprites = self.obstacle_sprites
		self.player.create_attack = self.create_attack
		self.player.destroy_attack = self.destroy_attack
		self.player.create_magic = self.create_magic
		self.player.barra.display_surface = self.display_surface
  
		self.player.hitbox.topleft = self.posInit
	def create_attack(self):
		
		self.current_attack = Weapon(self.player,[self.visible_sprites,self.attack_sprites])

	def create_magic(self,style,strength,cost):
		if style == 'heal':
			self.magic_player.heal(self.player,strength,cost,[self.visible_sprites])

		if style == 'flame':
			self.magic_player.flame(self.player,cost,[self.visible_sprites,self.attack_sprites])
		if style == 'ray':
			self.magic_player.ray(self.player,cost,[self.visible_sprites,self.attack_sprites])
		if style == 'magic':
			self.magic_player.magic(self.player,cost,[self.visible_sprites,self.attack_sprites])

	def drop_item(self, pos):
		materiales = ["bateria","cuerdas","cables","madera"]
		eleccion = random.choice(materiales)
		Item([self.visible_sprites],  eleccion, pos, self.display_surface, player = self.player)

	def destroy_attack(self):
		if self.current_attack:
			self.current_attack.kill()
		self.current_attack = None

	def player_attack_logic(self):
		if self.attack_sprites:
			for attack_sprite in self.attack_sprites:
				collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
				if collision_sprites:
					for target_sprite in collision_sprites:
						if target_sprite.sprite_type == 'grass':
							pos = target_sprite.rect.center
							offset = pygame.math.Vector2(0,75)
							for leaf in range(randint(3,6)):
								self.animation_player.create_grass_particles(pos - offset,[self.visible_sprites])
							target_sprite.kill()
						else:
							target_sprite.get_damage(self.player,attack_sprite.sprite_type)

	def damage_player(self,amount,attack_type):
		if self.player.vulnerable:
			self.player.health -= amount
			self.player.vulnerable = False
			self.player.hurt_time = pygame.time.get_ticks()
			self.animation_player.create_particles(attack_type,self.player.rect.center,[self.visible_sprites])

	def trigger_death_particles(self,pos,particle_type):

		self.animation_player.create_particles(particle_type,pos,self.visible_sprites)

	def add_exp(self,amount):

		self.player.exp += amount

	def toggle_menu(self):

		self.game_paused = not self.game_paused 

	def run(self):
		self.visible_sprites.custom_draw(self.player)
		self.ui.display()
		self.visible_sprites.logros.updateNota()
		if self.game_paused:
			self.upgrade.display()
		else:
			self.visible_sprites.update()
			self.visible_sprites.enemy_update(self.player)
			self.visible_sprites.npc_update(self.player)

			self.player_attack_logic()


class Level_2 (Level):
    def __init__(self, player=None):
        super().__init__(2, "ground 2", 4, player)

class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self, tile, scale=1):
		from enemy import Enemy
		from Npc import NPC
		# general setup 
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2
		self.offset = pygame.math.Vector2()
		self.logros = Logros(self.display_surface)
		# creating the floor
		self.floor_surf = pygame.image.load(f'graphics/tilemap/{tile}.png').convert()
		self.floor_surf = pygame.transform.scale(self.floor_surf, (self.floor_surf.get_width()*scale,self.floor_surf.get_height()*scale))
		self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

	def custom_draw(self,player):

		# getting the offset 
		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height

		# drawing the floor
		floor_offset_pos = self.floor_rect.topleft - self.offset
		self.display_surface.blit(self.floor_surf,floor_offset_pos)

		# for sprite in self.sprites():
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image,offset_pos)


	def enemy_update(self,player):
		enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
		for enemy in enemy_sprites:
			enemy.enemy_update(player)
			#BARRRA DE VIDA HERE
	
	def npc_update(self, player):
		npc_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'npc']
		for npc in npc_sprites:
			npc.npc_update(player)

	def obtener_posRespecto_camara(self, objetoEntity):
		self.offset.x = objetoEntity.rect.centerx - self.half_width
		self.offset.y = objetoEntity.rect.centery - self.half_height
		return(self.offset.x, self.offset.y)
	
	def get_offset(self):
		return(self.offset)
	
