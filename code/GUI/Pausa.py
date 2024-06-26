import pygame, settings, sys
from pygame.locals import *
from GUI.button import Button  
from GUI.Range import Range  
from tkinter import messagebox
from GUI.Almanaque import Almanaque
from GUI.Controles import MenuControles
from DB import validar
from DB.conectar import *
from item import Item

class PausaMenu:
    def __init__(self, main_sound, pause_sound, player,conexion,cursor, screen = pygame.display.set_mode((settings.SCREEN_WIDTH,settings.SCREEN_HEIGHT))):
        self.screen = screen
        self.paused = True
        self.almanaque = None
        self.sound = main_sound
        self.pause_sound = pause_sound
        self.player = player
        self.conexion = conexion
        self.cursor = cursor
        
    def show_menu(self, screen):

        fontsito = pygame.font.Font('graphics/font/joystix.ttf', 20)
        self.screen.fill((50, 50, 50))

        menu_text = fontsito.render("MENU PAUSA", True, "white")
        menu_rect = menu_text.get_rect(center=(settings.SCREEN_WIDTH/2, settings.SCREEN_HEIGHT/11))

        fondo = pygame.image.load("graphics/elementos_graficos/pausa.png")
        fondo = pygame.transform.scale(fondo, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

        play_button = Button(image=settings.botonBlue, pos=(130, 220), text_input="Reanudar", font=fontsito,
                             base_color="#4D4D5C", hovering_color="#75E2EC")
        pokedex_button = Button(image=settings.botonRed, pos=(350, 220), text_input="Almanaque", font=fontsito,
                                base_color="#4D4D5C", hovering_color="#75E2EC")
        controles_button = Button(image=settings.botonGreen, pos=(350, 360), text_input="Controles", font=fontsito, 
                                  base_color="#4D4D5C", hovering_color="#75E2EC")
        salir_button = Button(image=settings.botonBlue, pos=(130, 500), text_input="Salir", font=fontsito,
                             base_color="#4D4D5C", hovering_color="#75E2EC")
        guardar_button = Button(image=settings.botonPur, pos=(130,360), text_input="Guardar partida", font=fontsito,
                                base_color="#4D4D5C", hovering_color="#75E2EC")
        
        range_volumen = Range((900, 650, 250, 22), "Musica")
        range_volumen.range = self.sound.music.get_volume() * 10
    

        
        #Soporte ks
        soporte_ks = Button(image=settings.botonSoporte, pos=(1100,670), text_input="", font=fontsito, base_color="#4D4D5C",
                          hovering_color="#C66FF1", link="https://nicolasayalagomez.github.io/FASTSTERNLANDING/#box6")
        
        
        while self.paused:
            
            self.screen.blit(fondo, (0, 0))
            self.screen.blit(menu_text, menu_rect)           

            soporte_ks.cargar(self.screen)
            
            controles_button.cargar(self.screen)
            
            play_button.cargar(self.screen)
            play_button.cambiar_color(pygame.mouse.get_pos())
  
            pokedex_button.cargar(self.screen)
            pokedex_button.cambiar_color(pygame.mouse.get_pos())
            
            salir_button.cargar(self.screen)
            salir_button.cambiar_color(pygame.mouse.get_pos())

            guardar_button.cargar(self.screen)
            guardar_button.cambiar_color(pygame.mouse.get_pos())

            #Volumen
            self.sound.music.set_volume(range_volumen.range/10)
            self.pause_sound.set_volume(range_volumen.range/10)

            events = pygame.event.get()

            range_volumen.draw(self.screen, events)

            for event in events:
                #Salir
                if event.type == pygame.QUIT:
                    respuesta = messagebox.askyesno("Precaución", "Se perderán los avances de este nivel. ¿Estás seguro?")
                    if respuesta:
                        pygame.quit()
                        sys.exit()
                #Renaudar
                if event.type == pygame.KEYDOWN:
                    if event.key == K_p or event.key == K_ESCAPE:
                        self.paused = False
                        play_button.click(self.screen)
                        self.pause_sound.stop()
                        return self.paused
                
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                 
                        #Accion del boton play
                    if play_button.checkForInput(pygame.mouse.get_pos()):
                        self.paused = False
                        play_button.click(self.screen)
                        self.pause_sound.stop()
                            
                        return self.paused
                        #Accion del boton guardar
                    if guardar_button.checkForInput(pygame.mouse.get_pos()):
                        print("Guardando")
                        lista = Item.valor(self)
                        validar.insertar_items(lista,self.conexion,self.cursor)

                        #Accion del boton almanaque
                    if pokedex_button.checkForInput(pygame.mouse.get_pos()):
                        self.paused = False
                        pokedex_button.click(self.screen)
                        self.alm = Almanaque(screen, self.player, 'graphics/elementos_graficos/fondosgenerico.png', rect=(settings.SCREEN_WIDTH,settings.SCREEN_HEIGHT),center=True) #listaMateriales = player.itemsRecolectados
                        Elpepe = self.alm.show_almanaque(screen)
                        if Elpepe == False:
                            self.pause_sound.stop()                          
                        return self.paused
                    
                    #accion del boton controles
                    if controles_button.checkForInput(pygame.mouse.get_pos()):
                        self.paused = False
                        controles_button.click(self.screen)
                        self.cont = MenuControles(screen, 'graphics/elementos_graficos/fondosgenerico.png', rect=(settings.SCREEN_HEIGHT, settings.SCREEN_WIDTH), center=True)
                        Elpepe2 = self.cont.show_menu_controles(screen)
                        if Elpepe2 == False:
                            self.pause_sound.stop()
                        return self.paused

                    if soporte_ks.checkForInput(pygame.mouse.get_pos()):
                        soporte_ks.click(self.screen)

                    if salir_button.checkForInput(pygame.mouse.get_pos()):
                        salir_button.click(self.screen)
                        respuesta = messagebox.askyesno("Precaución", "Se perderán los avances de este nivel. ¿Estás seguro?")
                        if respuesta:
                            pygame.quit()
                            sys.exit()

            pygame.display.update()
