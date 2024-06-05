import pygame

class BurbujaTexto():
    def __init__(self,screen):
        pygame.init()
        self.display_surface = screen

        self.barra_vida= pygame.image.load("graphics/elementos_graficos/barra.png").convert_alpha()
        self.barra_vida = pygame.transform.scale(self.barra_vida, (86,23))

        self.barra_vida_rect= self.barra_vida.get_rect()
        self.bar_x = 0
        self.bar_y = 0
        self.flag = False

        self.barra_vida_relleno = (self.bar_x+17,(self.bar_y+self.barra_vida_rect.height//2))
        self.barra_max_ancho = 62 #pixeles
        self.barra_alto = 2

    def mostrar_interaccion(self,objetoEntity):
        self.objetoEntity = objetoEntity

        self.display_surface.blit(self.barra_vida,(self.bar_x, self.bar_y))
        self.objetoEntity.updateMess(self.display_surface)