import pygame, settings
from GUI.button import Button
from settings import *

class Mezcladora():
    def __init__(self,screen, pausa): #= pygame.display.set_mode((settings.SCREEN_WIDTH,settings.SCREEN_HEIGHT))
        #self.lista_consumir = lista
        self.mezcladora = True
        self.screen = screen
        self.paused = pausa
        
        
    def mostrar_menu_mezcladora(self):
        
        fontsito = pygame.font.Font('graphics/font/joystix.ttf', 20)
        
        boton_regresar = Button(image=settings.botonRegresar, pos=(200,160),text_input="", font=fontsito,
                             base_color="#4D4D5C", hovering_color="#75E2EC")
    
        fondo = pygame.image.load("graphics/elementos_graficos/fondosgenerico.png")
        fondo = pygame.transform.scale(fondo, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

        while self.mezcladora:
            self.screen.fill((50,50,50))
            self.screen.blit(fondo,(0,0))

            boton_regresar.cargar(self.screen)

            events = pygame.event.get()

            for event in events:

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if boton_regresar.checkForInput(pygame.mouse.get_pos()):
                        boton_regresar.click(self.screen)
                        self.mezcladora = False
                        return self.mezcladora
                    
            pygame.display.update()
