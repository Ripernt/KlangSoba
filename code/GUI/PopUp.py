import pygame

from GUI.Boton import Boton

from GUI.Gradient import GradientSurface

from GUI.Secciones import SeccionesTexto

from GUI.Parrafo import Parrafo

from GUI.Label import Label

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
BLUE = (0, 0, 200)
ORANGE = (246, 144, 26)
GREEN = (39, 183, 20)

class PopUp:
    def __init__(self, screen, width, height, title, image, font = None, nombreCien = "", nombre = "", descripcion = "", parametros = ["", "", ""], tipo = False, colorD = (0,0,0), num_especies = 0):
        self.width = width
        self.height = height
        self.title = title


        self.enabled = False
        
        self.screen = screen

        if font is None:
            self.font = pygame.font.Font("Fonts/ARCADECLASSIC.TTF", 25)
            self.font.set_bold(False)
            self.fontsito = pygame.font.Font("Fonts/ARCADECLASSIC.TTF", 15)
            self.fontsito.set_bold(False)
            self.fontsito2 = pygame.font.Font("Fonts/RobotoMono-VariableFont_wght.TTF", 12)
            self.fontsito2.set_bold(False)
        else:
            self.fontsito = font
            self.font = font

        self.cortina = pygame.Surface((screen.get_width(), screen.get_height())).convert_alpha()
        self.cortina.fill((0,0,0,100))

        # Crea una superficie para el pop-up con un borde negro.
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(WHITE)
        
        # Crea una superficie para la sombra con degradado.
        self.shadow_surface = pygame.Surface((self.width + 20, self.height + 20), pygame.BLEND_RGBA_ADD).convert_alpha()
        self.shadow_surface.fill((0, 0, 0, 0))
        
        # Dibuja la sombra con degradado en la superficie de sombra.
        for i in range(10,1, -1):
            alpha = int((1.0 - i / 10.0) * 255)
            color = (0, 0, 0)
            pygame.draw.rect(self.shadow_surface, color + (alpha,), pygame.Rect(i+1, i+1, self.width-2, self.height-2))

        self.centerx = self.screen.get_width()//2-self.width//2
        self.centery = self.screen.get_height()//2-self.height//2
        self.buttonExit = Boton((self.centerx+self.width -30,self.centery+ 10,20,20), "X", [(255,255,255),(255,255,255)], text_color=(255,255,255))

        rel = 120/image.get_height()
        self.imageAn = pygame.transform.scale(image, (image.get_width()*rel, image.get_height()*rel))
        
        self.nombreCien = nombreCien
        self.nombre = nombre
        self.descripcion = descripcion
        self.parametros = parametros
        self.tipo = tipo

        self.textDes = Parrafo(self.descripcion, self.fontsito2, GRAY, 260)

        self.labelEspecimemes = Label(f"Recogidos: {num_especies}", "Fonts/RobotoMono-VariableFont_wght.TTF", 12, (0,80,90,25), text_color=(0,0,0), align="center")

        if tipo:
            parametrosDefault = ["COLOR", "ESPINAS", "REPRODUCCION"]
        else:
            parametrosDefault = ["SALTO", "VELOCIDAD", "AGILIDAD"]
        
        self.COLORKEY = colorD

        textos = [parametros[0], parametrosDefault[0], parametros[1], parametrosDefault[1], parametros[2], parametrosDefault[2]]

        self.prop = SeccionesTexto(self.COLORKEY, textos,  (300,68))

        self.bgR = GradientSurface(300, 100, (self.COLORKEY[0],self.COLORKEY[1],self.COLORKEY[2], 255))

        
        
        
    def show(self, events):
        if self.enabled:
            
            self.screen.blit(self.cortina, (0,0))

            # Dibuja la sombra con degradado detrás del pop-up.
            self.screen.blit(self.shadow_surface, (self.centerx,self.centery))
            # self.surface.blit(self.bg, (0,0))
            self.bgR.draw(self.surface, (0, 0))
            # Dibuja el pop-up en la pantalla.






            self.screen.blit(self.surface, (self.centerx,self.centery))







            self.surface.fill((255,255,255))
            


            self.screen.blit(self.imageAn, self.imageAn.get_rect(center=(self.width//2+self.centerx, self.imageAn.get_height()//2+self.centery-50)))

            self.labelEspecimemes.update(self.surface)

            self.buttonExit.update(self.screen, events)
            
            if self.buttonExit.is_clicked(events):
                self.enabled = False


            # Agrega el título y el texto en el pop-up.
            title_text = self.fontsito.render(self.nombreCien, False, self.COLORKEY)
            title_rect = title_text.get_rect(center=(self.surface.get_rect().centerx, self.surface.get_rect().top + 120))
            self.surface.blit(title_text, title_rect)

            
            title_text = self.font.render(self.nombre, False, BLACK)
            title_rect = title_text.get_rect(center=(self.surface.get_rect().centerx, self.surface.get_rect().top + 140))
            self.surface.blit(title_text, title_rect)

            self.surface.blit(self.textDes.surface, self.textDes.surface.get_rect(center=(self.width//2, self.textDes.surface.get_height()//2+160)))

            self.prop.draw(self.surface, (0,self.height-self.prop.size[1]))



            
        
    def clicksEvent(self, events):
        clicks = []
        if self.enabled:
            for i, El in enumerate(self.Elements):
                if El.is_clicked(events, self.centerx, self.centery):
                    clicks.append((i,El.title))
        return clicks

    def add(self, widget):
        if widget is not None:
            widget.screen = self.surface
            self.Elements.append(widget)
    
    def active(self):
        self.enabled = True


