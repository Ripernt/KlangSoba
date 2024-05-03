import pygame, settings, sys
from pygame.locals import *
from GUI.button import Button  
from GUI.Range import Range  
from tkinter import messagebox
from GUI.Almanaque import Almanaque
from GUI.MenuMezcladora import Mezcladora
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

        play_button = Button(image=settings.botonBlue, pos=(200, 160), text_input="Reanudar", font=fontsito,
                             base_color="#4D4D5C", hovering_color="#75E2EC")
        pokedex_button = Button(image=settings.botonRed, pos=(200, 300), text_input="Almanaque", font=fontsito,
                                base_color="#4D4D5C", hovering_color="#75E2EC")
        salir_button = Button(image=settings.botonGreen, pos=(200, 440), text_input="Salir", font=fontsito,
                             base_color="#4D4D5C", hovering_color="#75E2EC")
        guardar_button = Button(image=settings.botonBlue, pos=(200,580), text_input="Guardar partida", font=fontsito,
                                base_color="#4D4D5C", hovering_color="#75E2EC")
        mezcladora_button = Button(image=settings.botonBlue, pos=(600,440), text_input="Mezcladora",font=fontsito,
                                base_color="#4D4D5C", hovering_color="#75E2EC")
        
        mezcladora_costo = 1
        permiso_mezcladora = False
        
        range_volumen = Range((900, 650, 250, 22), "Musica")
        range_volumen.range = self.sound.music.get_volume() * 10
    
        
        
        while self.paused:
            
            self.screen.blit(fondo, (0, 0))
            self.screen.blit(menu_text, menu_rect)
            
            #Mostrar boton de play
            play_button.cargar(self.screen)
            play_button.cambiar_color(pygame.mouse.get_pos())

            #Mostrar boton del almanaque
            pokedex_button.cargar(self.screen)
            pokedex_button.cambiar_color(pygame.mouse.get_pos())
            #Mostrar boton de salir 
            salir_button.cargar(self.screen)
            salir_button.cambiar_color(pygame.mouse.get_pos())

            #Mostrar boton de guardar partida
            guardar_button.cargar(self.screen)
            guardar_button.cambiar_color(pygame.mouse.get_pos())

            #Mostrar boton para la mezcladora (PRUEBA)
            mezcladora_button.cargar(self.screen)
            mezcladora_button.cambiar_color(pygame.mouse.get_pos())

            #Volumen
            self.sound.music.set_volume(range_volumen.range / 10)
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
                    #if self.almanaque is None:
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
                        
                        #Accion para entrar al menu Mezcladora
                    if mezcladora_button.checkForInput(pygame.mouse.get_pos()):
                        if mezcladora_costo <= self.player.items_num[0] and permiso_mezcladora == False:
                            constante = self.player.items_num[0] - mezcladora_costo
                            self.player.items_num[0] = constante
                            permiso_mezcladora = True
                            validar.insertar_items(self.player.items_num, self.conexion, self.cursor)
                        else:
                            print("Necesitas mas items para usar la mezcladora")
                        
                        if permiso_mezcladora == True:
                            self.paused = False
                            mezcladora_button.click(self.screen)   
                            self.mez = Mezcladora(self.screen,self.paused)
                            nose = self.mez.mostrar_menu_mezcladora()
                            if nose == False:
                                self.pause_sound.stop()
                            return self.paused

                    if salir_button.checkForInput(pygame.mouse.get_pos()):
                        salir_button.click(self.screen)
                        respuesta = messagebox.askyesno("Precaución", "Se perderán los avances de este nivel. ¿Estás seguro?")
                        if respuesta:
                            pygame.quit()
                            sys.exit()

            pygame.display.update()
