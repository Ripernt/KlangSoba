import pygame
from GUI.button2 import Button2
from GUI.button import Button

class InterfazSintetizador:

    def __init__(self, screen, instrumentos):
        self.instrumentos = instrumentos
        self.screen = screen
        self.sintetizador = True
        self.fontsito = pygame.font.Font('graphics/font/joystix.ttf', 20)


    def mostrar_menu_sintetizador(self):
        self.screen.fill((50,50,50))
        #Boton salir
        boton=pygame.image.load("graphics/elementos_graficos/botonT.png")
        boton=pygame.transform.scale(boton,(50,50))
        self.salir_botton = Button(image=boton, pos=(100,100), text_input="",font=self.fontsito,base_color="#4D4D5C",hovering_color="#75E2EC")

        while self.sintetizador:

            self.salir_botton.cargar(self.screen)
            self.salir_botton.cambiar_color(pygame.mouse.get_pos())

            events = pygame.event.get()
            for event in events:
                #Salir
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.salir_botton.checkForInput(pygame.mouse.get_pos()):
                        self.sintetizador = False
                        #self.instrumentos = True
                        self.salir_botton.click(self.screen)
                        #self.musica_almanaque.stop() //Agregar
                        return self.sintetizador

                pygame.display.update()
