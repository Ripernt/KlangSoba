import pygame
from pygame.locals import *
from GUI.button import Button  
from GUI.Range import Range  
import settings
import sys
from tkinter import messagebox

class PausaMenu:
    def __init__(self, main_sound, pause_sound, screen = pygame.display.set_mode((settings.SCREEN_WIDTH,settings.SCREEN_HEIGHT))):
        self.screen = screen
        self.paused = True
        self.almanaque = None
        self.sound = main_sound
        self.pause_sound = pause_sound
    def show_menu(self):

        fontsito = pygame.font.Font('graphics/font/joystix.ttf', 20)
        self.screen.fill((50, 50, 50))

        menu_text = fontsito.render("MENU PAUSA", True, "white")
        menu_rect = menu_text.get_rect(center=(settings.SCREEN_WIDTH/2, settings.SCREEN_HEIGHT/11))

        fondo = pygame.image.load("graphics/elementos_graficos/pausa.png")
        fondo = pygame.transform.scale(fondo, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

        play_button = Button(image=settings.botonBlue, pos=(200, 160), text_input="Reanudar", font=fontsito,
                             base_color="#4D4D5C", hovering_color="#75E2EC")
        pokedex_button = Button(image=settings.botonRed, pos=(200, 360), text_input="Almanaque", font=fontsito,
                                base_color="#4D4D5C", hovering_color="#75E2EC")
        salir_button = Button(image=settings.botonGreen, pos=(200, 560), text_input="Salir", font=fontsito,
                             base_color="#4D4D5C", hovering_color="#75E2EC")

        range_volumen = Range((900, 650, 250, 22), "Musica")
        range_volumen.range = self.sound.music.get_volume() * 10
       
        
        
        while self.paused:
            
            self.screen.blit(fondo, (0, 0))
            self.screen.blit(menu_text, menu_rect)
            
            play_button.cargar(self.screen)
            play_button.cambiar_color(pygame.mouse.get_pos())

            pokedex_button.cargar(self.screen)
            pokedex_button.cambiar_color(pygame.mouse.get_pos())

            salir_button.cargar(self.screen)
            salir_button.cambiar_color(pygame.mouse.get_pos())

            self.sound.music.set_volume(range_volumen.range / 10)
            self.pause_sound.set_volume(range_volumen.range/10)

            events = pygame.event.get()

            range_volumen.draw(self.screen, events)

            for event in events:
                if event.type == pygame.QUIT:
                    respuesta = messagebox.askyesno("Precaución", "Se perderán los avances de este nivel. ¿Estás seguro?")
                    if respuesta:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_p or event.key == K_ESCAPE:
                        self.paused = False
                        play_button.click(self.screen)
                        self.pause_sound.stop()
                        
                        return self.paused

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.almanaque is None:
                        if play_button.checkForInput(pygame.mouse.get_pos()):
                            self.paused = False
                            play_button.click(self.screen)
                            self.pause_sound.stop()
                            
                            return self.paused
                        elif pokedex_button.checkForInput(pygame.mouse.get_pos()):
                            
                            pokedex_button.click(self.screen)

                        elif salir_button.checkForInput(pygame.mouse.get_pos()):
                            salir_button.click(self.screen)
                            respuesta = messagebox.askyesno("Precaución", "Se perderán los avances de este nivel. ¿Estás seguro?")
                            if respuesta:
                                pygame.quit()
                                sys.exit()

            pygame.display.update()
