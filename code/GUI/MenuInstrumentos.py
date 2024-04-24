import pygame
from GUI.button import Button
from GUI.UIPiano import InterfazPiano
import settings
from pygame.locals import *
from DB import validar
from settings import *

class MInstrumentos:
    def __init__(self, main_sound, musica_bass, lista,player,conexionR,cursorR,screen = pygame.display.set_mode((settings.SCREEN_WIDTH,settings.SCREEN_HEIGHT))):
        
        self.lista = lista
        self.screen = screen
        self.instrumentos = True
        self.sound = main_sound
        self.musicap = musica_bass
        self.player = player
        self.conexion = conexionR
        self.cursor = cursorR
        
    def carga_instrumento(self,instrumento):
        self.player.T_piano = instrumento
         

    def mostrar_instrumentos(self):
        #CV2 liberias para modificar las imagenes |open cv --python
        
        piano_costo = 3
        sintetizador_costo = 3

        fonti = pygame.font.Font('graphics/font/joystix.ttf', 20)
        self.screen.fill((50,50,50))

        instrumentos_text = fonti.render("Menu de instrumentos", True, "white") 
        instrumentos_rect = instrumentos_text.get_rect(center=(settings.SCREEN_WIDTH/2, settings.SCREEN_HEIGHT/11))

        piano_Button = Button(image=settings.botonPiano, pos=(420,275), text_input="", font=fonti, base_color="#FFFFFF", hovering_color="#75E2EC")
        
        sintetizador_Button = Button(image=settings.botonSintetizador, pos=(820,275), text_input="", font=fonti, base_color="#FFFFFF", hovering_color="#75E2EC")
        fondo = pygame.image.load("graphics/elementos_graficos/Menuinstrumentos.png")
        fondo = pygame.transform.scale(fondo, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

        regresar_button = Button(image=settings.botonRegresar, pos=(200, 600), text_input="", font=fonti,
        base_color="#4D4D5C", hovering_color="#75E2EC")

        #Boton piano bloqueado
        piano_bloqueado = Button(image=settings.botonPianoBloqueado, pos=(420,275), text_input="", font=fonti, base_color="#FFFFFF", hovering_color="#75E2EC")
        sintetizador_bloqueado = Button(image=settings.botonSintetizadorBloqueado, pos=(820,275), text_input="", font=fonti, base_color="#FFFFFF", hovering_color="#75E2EC")

        self.fontsito = pygame.font.Font('graphics/font/pixelart.TTF', 20)  
        self.screen.fill((50,50,50))

        #Items para el instrumento piano
        madera_text = self.fontsito.render("x"+str(piano_costo), True, "white") 
        piano_text = self.fontsito.render("Piano", True, "white")
        madera_img = pygame.image.load("graphics/items/madera.png")
        madera_img = pygame.transform.scale(madera_img,(50,50))
                #Items para el instrumento sintetizador
        pila_text = self.fontsito.render("x"+str(sintetizador_costo), True, "white")
        sintetizador_text = self.fontsito.render("Sintetizador", True, "white")
        pila_img = pygame.image.load("graphics/items/bateria.png")
        pila_img = pygame.transform.scale(pila_img,(50,50))
        renderT = None
        
        while self.instrumentos:

            """#Mostrar piano y sintetizador
            if piano_bloqueado is not None:
                piano_bloqueado.cargar
                piano_bloqueado.cambiar_color(pygame.mouse.get_cursor())
            elif piano_bloqueado is None:
                piano_Button.cargar(self.screen)
                piano_Button.cambiar_color(pygame.mouse.get_cursor())
                
            if sintetizador_bloqueado is not None:
                sintetizador_bloqueado.cargar(self.screen)
                sintetizador_bloqueado.cambiar_color(pygame.mouse.get_cursor())
            elif sintetizador_bloqueado is None:
                sintetizador_Button.cargar(self.screen)
                sintetizador_Button.cambiar_color(pygame.mouse.get_cursor())"""
            #Valida si tiene el instrumento piano
            """if self.player.T_piano[0] == 1:
                no_tiene_piano = True
            else:
                no_tiene_piano = False
            #Valida si tiene el instrumento sintetizador
            if self.player.T_piano[1] == 1:
                no_tiene_sintetizador = True
            else:
                no_tiene_sintetizador = False"""

            self.screen.blit(fondo, (0,0))
            self.screen.blit(instrumentos_text, instrumentos_rect)
            if renderT is not None:
                self.screen.blit(renderT, rect)

            #Mostrar boton regresar    
            regresar_button.cargar(self.screen)
            regresar_button.cambiar_color(pygame.mouse.get_pos())

            #Mostrar boton bloqueado o desbloqueado
            if self.player.T_piano[0] == 1:
                piano_bloqueado.cargar(self.screen)
                piano_bloqueado.cambiar_color(pygame.mouse.get_pos())
            else:
                #Mostrar boton piano
                piano_Button.cargar(self.screen)
                piano_Button.cambiar_color(pygame.mouse.get_pos())
            if self.player.T_piano[1] == 1:
                sintetizador_bloqueado.cargar(self.screen)
                sintetizador_bloqueado.cambiar_color(pygame.mouse.get_pos())
            else:
                #Mostrar boton sintetizador
                sintetizador_Button.cargar(self.screen)
                sintetizador_Button.cambiar_color(pygame.mouse.get_pos())


            
            #Mostrar items para el instrumento piano
            if self.player.T_piano[0] == 1:
                self.screen.blit(madera_img,(365,390))
                self.screen.blit(madera_text,(420,400))
            else:
                self.screen.blit(piano_text,(390,400))
             
                
            
            #Mostrar items para el instrumento sintetizador
            if self.player.T_piano[1] == 1:
                self.screen.blit(pila_img,(765,390))
                self.screen.blit(pila_text,(820,400))
            else:
                self.screen.blit(sintetizador_text,(770,400))

            evento = pygame.event.get()


            for event in evento:
            
                if event.type == pygame.KEYDOWN:
                    if event.key == K_m or event.key == K_ESCAPE:
                        self.instrumentos = False
                        regresar_button.click(self.screen)
                        self.sound.pause()
                        self.musicap.stop()
                        return self.instrumentos
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if regresar_button.checkForInput(pygame.mouse.get_pos()):
                        self.instrumentos = False
                        regresar_button.click(self.screen)
                        self.sound.pause()
                        self.musicap.stop()
                        return self.instrumentos
                    
                    if self.player.T_piano[0] == 1:

                        if piano_Button.checkForInput(pygame.mouse.get_pos()):  
                            print("Items madera: ", self.lista[3])
                            if piano_costo <= self.lista[3]:
                                self.player.T_piano[0] = 2
                                constante = self.lista[3] - piano_costo
                                self.lista[3] = constante
                                print(self.lista[3])
                                print(self.player.T_piano[0])
                                #Actualiza los items del usuario al desbloquear el piano
                                validar.insertar_items(self.lista,self.conexion,self.cursor)
                                print("desbloqueado: ", self.player.T_piano[0])
                                #Instroduce el piano desbloqueado en la base de datos
                                validar.instrumento_piano(self.player.T_piano,self.conexion,self.cursor)
                                
                                
                            else:
                                a = "No se tienen suficientes items"
                                textR = pygame.font.Font("graphics/font/joystix.ttf", 15)
                                renderT = textR.render(a, True, (255,0,0))
                                rect = renderT.get_rect(center=(SCREEN_WIDTH//2, 430))                                 
                        
                    else:

                        if piano_Button.checkForInput(pygame.mouse.get_pos()):
                            self.instrumentos = False
                            piano_Button.click(self.screen)
                            self.inst = InterfazPiano(self.screen, self.instrumentos)
                            self.sound.pause()
                            self.musicap.stop()
                            eee = self.inst.mostrar_menu_piano()
                            if eee == False:
                                self.musicap.stop()
                            return self.instrumentos 
                
                        

            pygame.display.update()
                
