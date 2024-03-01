import pygame
import settings
from random import randint


# Iniciamos pygame
pygame.init()

class EfectoLuz:
    #constructor, toma como parametros(imagen de luz,tamaño de la ventana)
    def __init__(self, imagen_luz_path, window_size = [settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT]):
        pygame.init()
        self.window_size = window_size
        # Crea la ventana principal
        self.screen = pygame.display.set_mode(window_size)
        # Carga la imagen de la luz y la escala
        self.image = pygame.image.load(imagen_luz_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (window_size[1], window_size[1]))
        # Crea un objeto Surface sobre el cual se va crear el efecto de luz con la imagen (se le asigna el tamaño de la imagen de la luz)
        self.luz = pygame.Surface(self.image.get_size()).convert_alpha()
        # Se llena de color negro
        self.luz.fill((0, 0, 0))
        # Dibuja la imagen de luz en el objeto Surface negro
        self.luz.blit(self.image, (0, 0))
        # Recorre todos los píxeles del objeto Surface negro y remplaza los pixeles blancos de la imagen de la luz por pixeles negros transparentes
        # De manera que mientras mas blanco, mas transparente será el pixel negro
        for y in range(self.luz.get_height()):
            for x in range(self.luz.get_width()):
                p = self.luz.get_at((x, y))
                color = (0, 0, 0, 255-p[0])
                self.luz.set_at((x, y), color)
        # Ahora crea el Surface que corresponde a la sobra de la cueva por ejemplo y la llena de color negro
        self.sombra = pygame.Surface((self.window_size)).convert_alpha()
        self.sombra.fill((0, 0, 0))
        self.sombraMod = self.sombra.copy()

        self.luzParpadeo = []
        for i in range(40):
            self.luzParpadeo.append(pygame.transform.scale(self.luz, (460+i,460+i)))

    def pintarLuz(self,origenLuz):
        if origenLuz[0]+500>0 and origenLuz[0]-500<settings.SCREEN_WIDTH or True:
            # Hace una copia de la superficie recibida (que corresponde a una sombra)
            sup = self.sombraMod
            # sup = pygame.transform.scale(sup, size)
            luz = self.luzParpadeo[randint(0,len(self.luzParpadeo)-1)]
            # Saca el rectangulo de la luz para saber en donde dibujarlo (le asigna de centro el origen de la luz)
            luz_rect = luz.get_rect(center=origenLuz)
            # Ahora pinta sobre la copia de la superficie el efecto de luz creado. Hacemos uso de la bandera BLEND_RGBA_MULT
            # Para que cuando se remplacen los pixeles de la luz por los de la sombre (si no especificamos esta bandera, lo que va a hacer
            # es que se van a sobreponer las imagenes y la transparencia del efecto de luz se va a perder)
            sup.blit(luz, luz_rect, special_flags=pygame.BLEND_RGBA_MULT)
        
            # Retornamos la sombra resultante 
            return sup
        return self.sombra
    def restablecer(self):
        self.sombraMod = self.sombra.copy()

