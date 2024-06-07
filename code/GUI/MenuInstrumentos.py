import pygame
from GUI.button import Button
from GUI.UIPiano import InterfazPiano
from GUI.UISintetizador import InterfazSintetizador
from GUI.MenuMezcladora import Mezcladora
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
        
        piano_costo_madera = 4
        piano_costo_cuerda = 6
        
        sintetizador_costo_cables = 5
        sintetizador_costo_pilas = 8

        fonti = pygame.font.Font('graphics/font/joystix.ttf', 20)
        self.screen.fill((50,50,50))

        #Texto menu de instrumentos
        instrumentos_text = fonti.render("Menu de instrumentos", True, "white") 
        instrumentos_rect = instrumentos_text.get_rect(center=(settings.SCREEN_WIDTH/2, settings.SCREEN_HEIGHT/11))

        #Boton piano
        piano_Button = Button(image=settings.botonPiano, pos=(450,275), text_input="", font=fonti, base_color="#FFFFFF", hovering_color="#75E2EC")

        #Boton sintetizador
        sintetizador_Button = Button(image=settings.botonSintetizador, pos=(850,275), text_input="", font=fonti, base_color="#FFFFFF", hovering_color="#75E2EC")

        #Fondo de menu instrumentos
        fondo = pygame.image.load("graphics/elementos_graficos/Menuinstrumentos.png")
        fondo = pygame.transform.scale(fondo, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

        #Boton regresar
        regresar_button = Button(image=settings.botonRegresar, pos=(200, 600), text_input="", font=fonti,
        base_color="#4D4D5C", hovering_color="#75E2EC")

        #Boton piano bloqueado
        piano_bloqueado = Button(image=settings.botonPianoBloqueado, pos=(450,275), text_input="", font=fonti, base_color="#FFFFFF", hovering_color="#75E2EC")
        sintetizador_bloqueado = Button(image=settings.botonSintetizadorBloqueado, pos=(850,275), text_input="", font=fonti, base_color="#FFFFFF", hovering_color="#75E2EC")
    
        #Fuente de la letra
        self.fontsito = pygame.font.Font('graphics/font/pixelart.TTF', 20)  

        #Items para el instrumento piano
        madera_text = self.fontsito.render("x"+str(piano_costo_madera), True, "white")
        cuerda_text = self.fontsito.render("x"+str(piano_costo_cuerda),True, "white") 
        piano_text = self.fontsito.render("Piano", True, "white")
        madera_img = pygame.image.load("graphics/items/madera.png")
        madera_img = pygame.transform.scale(madera_img,(50,50))
        cuerda_img = pygame.image.load("graphics/items/cuerdas.png")
        cuerda_img = pygame.transform.scale(cuerda_img,(50,50))
        #Items para el instrumento sintetizador
        pila_text = self.fontsito.render("x"+str(sintetizador_costo_pilas), True, "white")
        cables_text = self.fontsito.render("x"+str(sintetizador_costo_cables), True, "white")
        sintetizador_text = self.fontsito.render("Sintetizador", True, "white")
        pila_img = pygame.image.load("graphics/items/bateria.png")
        pila_img = pygame.transform.scale(pila_img,(50,50))
        cable_img = pygame.image.load("graphics/items/cables.png")
        cable_img = pygame.transform.scale(cable_img,(50,50))
        
        renderT = None
        
        while self.instrumentos:
            if self.player.T_piano[0] == 1:
                no_tiene_piano = True
            else:
                no_tiene_piano = False
            
            if self.player.T_piano[1] == 1:
                no_tiene_sintetizador = True
            else:
                no_tiene_sintetizador = False

            self.screen.blit(fondo, (0,0))
            self.screen.blit(instrumentos_text, instrumentos_rect)

            if renderT is not None:
                self.screen.blit(renderT, rect)

            if no_tiene_sintetizador == True:
                
                sintetizador_bloqueado.cargar(self.screen)
                
                self.screen.blit(pila_img,(815,390))
                self.screen.blit(pila_text,(870,400))
                self.screen.blit(cable_img, (815,460))
                self.screen.blit(cables_text,(870,470))
            else:
                
                sintetizador_Button.cargar(self.screen)
                self.screen.blit(sintetizador_text,(770,400))

            
            if no_tiene_piano == True:
               
                piano_bloqueado.cargar(self.screen)

                self.screen.blit(madera_img,(405,390))
                self.screen.blit(madera_text,(455,400))
                self.screen.blit(cuerda_img,(405,460))
                self.screen.blit(cuerda_text,(455,470))
                
            else:
                #Mostrar boton piano
                piano_Button.cargar(self.screen)
                #piano_Button.cambiar_color(pygame.mouse.get_pos())
                self.screen.blit(piano_text,(400,400))

            #Mostrar boton regresar    
            regresar_button.cargar(self.screen)
            regresar_button.cambiar_color(pygame.mouse.get_pos())

            evento = pygame.event.get()

            for event in evento:
            
                if event.type == pygame.KEYDOWN:
                    
                    if event.key == K_m or event.key == K_ESCAPE:
                        self.instrumentos = False
                        regresar_button.click(self.screen)
                        self.sound.pause()
                        self.musicap.stop()
                        return self.instrumentos
                if event.type == pygame.MOUSEBUTTONDOWN:

                    if regresar_button.checkForInput(pygame.mouse.get_pos()):
                        self.instrumentos = False
                        regresar_button.click(self.screen)
                        self.sound.pause()
                        self.musicap.stop()
                        return self.instrumentos
                    
                    if sintetizador_bloqueado.checkForInput(pygame.mouse.get_pos()) and no_tiene_sintetizador == True:
                        
                        sintetizador_bloqueado.click(self.screen)
                        if sintetizador_costo_pilas <= self.lista[0] and sintetizador_costo_cables <= self.lista[1]:
                            self.player.T_piano[1] = 3
                            constante2 = self.lista[0] - sintetizador_costo_pilas
                            constante3 = self.lista[1] - sintetizador_costo_cables
                            self.lista[0] = constante2
                            self.lista[1] = constante3
                            validar.insertar_items(self.lista,self.conexion,self.cursor)
                            
                            validar.instrumento_piano(self.player.T_piano,self.conexion,self.cursor)

                        else:

                            text_no_sintetizador = "No se tienen suficientes items para el sintetizador"
                            textR = pygame.font.Font("graphics/font/joystix.ttf", 15)
                            renderT = textR.render(text_no_sintetizador, True, (255,0,0))
                            rect = renderT.get_rect(center=(SCREEN_WIDTH//2, 150))
             
                    elif sintetizador_Button.checkForInput(pygame.mouse.get_pos()) and no_tiene_sintetizador == False:
                        
                        self.instrumentos = False
                        sintetizador_Button.click(self.screen)
                        self.inst = InterfazSintetizador(self.screen, self.instrumentos)
                        self.sound.pause()
                        self.musicap.stop()
                        eee = self.inst.mostrar_menu_sintetizador()
                        if eee == False:
                            self.musicap.stop()         
                            return self.instrumentos 
                       
                    if piano_bloqueado.checkForInput(pygame.mouse.get_pos()) and no_tiene_piano == True:
                        
                        piano_bloqueado.click(self.screen)
                        if piano_costo_madera <= self.lista[3] and piano_costo_cuerda <= self.lista[2]:
                            self.player.T_piano[0] = 2
                            constante = self.lista[3] - piano_costo_madera
                            constante4 = self.lista[2] - piano_costo_cuerda
                            self.lista[3] = constante
                            self.lista[2] = constante4
                            validar.insertar_items(self.lista,self.conexion,self.cursor)
                            
                            validar.instrumento_piano(self.player.T_piano,self.conexion,self.cursor)
                            
                        else:
                            
                            text_no_piano = "No se tienen suficientes items para el piano"
                            textR = pygame.font.Font("graphics/font/joystix.ttf", 15)
                            renderT = textR.render(text_no_piano, True, (255,0,0))
                            rect = renderT.get_rect(center=(SCREEN_WIDTH//2, 150))
                        
                    elif piano_Button.checkForInput(pygame.mouse.get_pos()) and no_tiene_piano == False:

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

                        
            
                
