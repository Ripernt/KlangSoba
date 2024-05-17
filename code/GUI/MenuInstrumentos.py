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
        #CV2 liberias para modificar las imagenes |open cv --python
        
        #Costo del intrumento piano
        piano_costo = 1
        #Costo del instrumento sintetizador
        sintetizador_costo = 1

        fonti = pygame.font.Font('graphics/font/joystix.ttf', 20)
        self.screen.fill((50,50,50))

        #Texto menu de instrumentos
        instrumentos_text = fonti.render("Menu de instrumentos", True, "white") 
        instrumentos_rect = instrumentos_text.get_rect(center=(settings.SCREEN_WIDTH/2, settings.SCREEN_HEIGHT/11))

        #Boton piano
        piano_Button = Button(image=settings.botonPiano, pos=(300,275), text_input="", font=fonti, base_color="#FFFFFF", hovering_color="#75E2EC")

        #Boton sintetizador
        sintetizador_Button = Button(image=settings.botonSintetizador, pos=(600,275), text_input="", font=fonti, base_color="#FFFFFF", hovering_color="#75E2EC")

        #Fondo de menu instrumentos
        fondo = pygame.image.load("graphics/elementos_graficos/Menuinstrumentos.png")
        fondo = pygame.transform.scale(fondo, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

        #Boton regresar
        regresar_button = Button(image=settings.botonRegresar, pos=(200, 600), text_input="", font=fonti,
        base_color="#4D4D5C", hovering_color="#75E2EC")

        #Boton piano bloqueado
        piano_bloqueado = Button(image=settings.botonPianoBloqueado, pos=(300,275), text_input="", font=fonti, base_color="#FFFFFF", hovering_color="#75E2EC")
        sintetizador_bloqueado = Button(image=settings.botonSintetizadorBloqueado, pos=(600,275), text_input="", font=fonti, base_color="#FFFFFF", hovering_color="#75E2EC")
    
        #Fuente de la letra
        self.fontsito = pygame.font.Font('graphics/font/pixelart.TTF', 20)  
        #Pantalla
        #self.screen.fill((50,50,50))

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

        mezcladora_button = Button(image=settings.botonMezcladora, pos=(900,275), text_input="Mezcladora",font=fonti,
                                base_color="#4D4D5C", hovering_color="#75E2EC")
        
        renderT = None
        
        while self.instrumentos:

            #Valida si tiene el instrumento piano
            if self.player.T_piano[0] == 1:
                no_tiene_piano = True
            else:
                no_tiene_piano = False
            #Valida si tiene el instrumento sintetizador
            if self.player.T_piano[1] == 1:
                no_tiene_sintetizador = True
            else:
                no_tiene_sintetizador = False

            self.screen.blit(fondo, (0,0))
            self.screen.blit(instrumentos_text, instrumentos_rect)

            if renderT is not None:
                self.screen.blit(renderT, rect)

            if no_tiene_sintetizador == True:
                #Mostrar boton sintetizador bloqueado
                sintetizador_bloqueado.cargar(self.screen)
                #sintetizador_bloqueado.cambiar_color(pygame.mouse.get_pos())
                self.screen.blit(pila_img,(565,390))
                self.screen.blit(pila_text,(620,400))
                pass
            else:
                #Mostrar boton sintetizador
                sintetizador_Button.cargar(self.screen)
                #sintetizador_Button.cambiar_color(pygame.mouse.get_pos())
                self.screen.blit(sintetizador_text,(520,400))

            #Mostrar boton bloqueado o desbloqueado
            if no_tiene_piano == True:
               
                piano_bloqueado.cargar(self.screen)
                #piano_bloqueado.cambiar_color(pygame.mouse.get_pos())
                self.screen.blit(madera_img,(255,390))
                self.screen.blit(madera_text,(305,400))
                
            else:
                #Mostrar boton piano
                piano_Button.cargar(self.screen)
                #piano_Button.cambiar_color(pygame.mouse.get_pos())
                self.screen.blit(piano_text,(260,400))

            #Mostrar boton regresar    
            regresar_button.cargar(self.screen)
            regresar_button.cambiar_color(pygame.mouse.get_pos())

            #Mostrar boton para la mezcladora (PRUEBA)
            mezcladora_button.cargar(self.screen)
            mezcladora_button.cambiar_color(pygame.mouse.get_pos())

            evento = pygame.event.get()

            for event in evento:
            
                if event.type == pygame.KEYDOWN:
                    #Accion regresar por medio de teclas
                    if event.key == K_m or event.key == K_ESCAPE:
                        self.instrumentos = False
                        regresar_button.click(self.screen)
                        self.sound.pause()
                        self.musicap.stop()
                        return self.instrumentos
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #Accion regresar por medio del boton
                    if regresar_button.checkForInput(pygame.mouse.get_pos()):
                        self.instrumentos = False
                        regresar_button.click(self.screen)
                        self.sound.pause()
                        self.musicap.stop()
                        return self.instrumentos
                    
                    if sintetizador_bloqueado.checkForInput(pygame.mouse.get_pos()) and no_tiene_sintetizador == True:
                        #print("Sintetizador bloqueadin")
                        sintetizador_bloqueado.click(self.screen)
                        if sintetizador_costo <= self.lista[0]:
                            self.player.T_piano[1] = 3
                            constante2 = self.lista[0] - sintetizador_costo
                            self.lista[0] = constante2
                            validar.insertar_items(self.lista,self.conexion,self.cursor)
                            #print("desbloqueado: ", self.player.T_piano[1])
                            validar.instrumento_piano(self.player.T_piano,self.conexion,self.cursor)
                            #if self.player.T_piano[1] == 3:
                            #    no_tiene_sintetizador = False
                        else:
                            #print("No se tienen suficientes items para el sintetizador")
                            text_no_sintetizador = "No se tienen suficientes items para el sintetizador"
                            textR = pygame.font.Font("graphics/font/joystix.ttf", 15)
                            renderT = textR.render(text_no_sintetizador, True, (255,0,0))
                            rect = renderT.get_rect(center=(SCREEN_WIDTH//2, 150))
             
                    elif sintetizador_Button.checkForInput(pygame.mouse.get_pos()) and no_tiene_sintetizador == False:
                        #print("Pianopianito no bloqueado")
                        #print("piano: ", no_tiene_piano)
                        #print("sintetizador: ", no_tiene_sintetizador)
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
                        #print("Pianopianito bloqueado")
                        piano_bloqueado.click(self.screen)
                        if piano_costo <= self.lista[3]:
                            self.player.T_piano[0] = 2
                            constante = self.lista[3] - piano_costo
                            self.lista[3] = constante
                            validar.insertar_items(self.lista,self.conexion,self.cursor)
                            #print("desbloqueado: ", self.player.T_piano[0])
                            validar.instrumento_piano(self.player.T_piano,self.conexion,self.cursor)
                            #if self.player.T_piano[0] == 2:
                            #    no_tiene_piano = False
                        else:
                            #print("No se tienen suficientes items para el piano")
                            text_no_piano = "No se tienen suficientes items para el piano"
                            textR = pygame.font.Font("graphics/font/joystix.ttf", 15)
                            renderT = textR.render(text_no_piano, True, (255,0,0))
                            rect = renderT.get_rect(center=(SCREEN_WIDTH//2, 150))
                        
                    elif piano_Button.checkForInput(pygame.mouse.get_pos()) and no_tiene_piano == False:
                        #print("Pianopianito no bloqueado")
                        #print("piano: ", no_tiene_piano)
                        #print("sintetizador: ", no_tiene_sintetizador)
                        self.instrumentos = False
                        piano_Button.click(self.screen)
                        self.inst = InterfazPiano(self.screen, self.instrumentos)
                        self.sound.pause()
                        self.musicap.stop()
                        eee = self.inst.mostrar_menu_piano()
                        if eee == False:
                            self.musicap.stop()
                                            
                            return self.instrumentos

                    #Accion para entrar al menu Mezcladora
                    if mezcladora_button.checkForInput(pygame.mouse.get_pos()):
                        self.instrumentos = False
                        mezcladora_button.click(self.screen)   
                        self.mez = Mezcladora(self.screen,self.instrumentos,self.player,self.conexion,self.cursor)
                        self.sound.pause()
                        self.musicap.stop()
                        nose = self.mez.mostrar_menu_mezcladora()
                        if nose == False:
                            self.musicap.stop()
                        return self.instrumentos 



            pygame.display.update()                            

                        
            
                
