import pygame
from entity import Entity


from math import sin
class Item(Entity):
    def __init__(self, groups, name, pos, surface, scale = 0.2, player=None):
        super().__init__(groups)
        
        self.image = pygame.image.load(f"graphics/items/{name}.png").convert_alpha()
        
        self.pos = pos
        
        self.player = player

        self.timeInit = pygame.time.get_ticks()
        
        self.image = pygame.transform.scale(self.image, ( int(round(self.image.get_width()*scale)), int(round(self.image.get_height()*scale)) ))


        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)
        
        self.pick_sound = pygame.mixer.Sound('audio/hit.wav')
        self.pick_sound.set_volume(0.3)
        
        self.name = name
        
        self.display_surface = surface

    def update(self):
        self.rect.y = self.pos[1] + sin((pygame.time.get_ticks()-self.timeInit)/200)*10 - 5
        if(pygame.time.get_ticks()-self.timeInit > 11000):
            self.kill()
            
            
        if(self.player.rect.colliderect(self.rect)):
            if self.name == "bateria":
                self.player.items_num[0]+=1
            elif self.name == "cables":
                self.player.items_num[1]+=1
            elif self.name == "cuerdas":
                self.player.items_num[2]+=1
            elif self.name == "madera":
                self.player.items_num[3]+=1
            
            
            print(f"recogiendo {self.name}")    
            print(self.player.items_num)
            self.kill()
        return self.player.items_num


    def valor(self):
        return self.player.items_num
    
    def carga_items(self, new_lista):

        self.player.items_num = new_lista
        
    
    
                
            