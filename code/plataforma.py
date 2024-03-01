import pygame 

class Plataforma:
    def __init__(self, center=[0,0], size = [50,50]):
        self.rect = pygame.Rect(center, size)
        self.rect.center =  center