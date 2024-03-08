import pygame
from GUI.button import Button
import settings
from pygame.locals import *
class MInstrumentos:
    def __init__(self, main_sound, musica_bass, screen = pygame.display.set_mode((settings.SCREEN_WIDTH,settings.SCREEN_HEIGHT))):

        self.screen = screen
        self.instrumentos = True
        self.sound = main_sound
        self.musicap = musica_bass

    def mostrar_instrumentos(self):

        fonti = pygame.font.Font('graphics/font/joystix.ttf', 20)
        self.screen.fill((50,50,50))

        instrumentos_text = fonti.render("Menu instrumentos", True, "white") 
        instrumentos_rect = instrumentos_text.get_rect(center=(settings.SCREEN_WIDTH/2, settings.SCREEN_HEIGHT/11))

        piano_Button = Button(image=settings.botonPiano, pos=(300,300), text_input="Piano", font=fonti, base_color="#FFFFFF", hovering_color="#75E2EC")
        sintetizador_Button = Button(image=settings.botonSintetizador, pos=(600,300), text_input="Sintetizador", font=fonti, base_color="#FFFFFF", hovering_color="#75E2EC")
        fondo = pygame.image.load("graphics/elementos_graficos/Menuinstrumentos.png")
        fondo = pygame.transform.scale(fondo, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

        regresar_button = Button(image=settings.botonBlue, pos=(1100, 600), text_input="Regresar", font=fonti,
        base_color="#4D4D5C", hovering_color="#75E2EC")
        
        while self.instrumentos:

            self.screen.blit(fondo, (0,0))
            self.screen.blit(instrumentos_text, instrumentos_rect)

            regresar_button.cargar(self.screen)
            regresar_button.cambiar_color(pygame.mouse.get_pos())

            sintetizador_Button.cargar(self.screen)
            sintetizador_Button.cambiar_color(pygame.mouse.get_pos())
            piano_Button.cargar(self.screen)
            piano_Button.cambiar_color(pygame.mouse.get_pos())

            evento = pygame.event.get()

            for event in evento:
            
                if event.type == pygame.KEYDOWN:
                    if event.key == K_m or event.key == K_ESCAPE:
                        self.instrumentos = False
                        regresar_button.click(self.screen)
                        self.sound.pause()
                        self.musicap.stop()
                        return self.instrumentos
                if event.type  == pygame.MOUSEBUTTONDOWN:
                    if regresar_button.checkForInput(pygame.mouse.get_pos()):
                        self.instrumentos = False
                        regresar_button.click(self.screen)
                        self.sound.pause()
                        self.musicap.stop()
                        return self.instrumentos

            pygame.display.update()
                
