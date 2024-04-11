import pygame

import numpy as np

from time import time

from GUI.PopUp import PopUp
from GUI.button import Button

class Almanaque():
    def __init__(self, screen,player, background,rect= None, center = False):
        self.screen = screen
        self.player = player
        if not center:
            self.rect = pygame.Rect(rect)
        else:
            self.rect = pygame.Rect(0,0,rect[0], rect[1])
            self.rect.center=(screen.get_width()//2, screen.get_height()//2)
            
        self.superficie = pygame.Surface((self.rect.width, self.rect.height))
        self.background = pygame.image.load(background)
        self.background = pygame.transform.scale(self.background,self.rect.size)

        self.almanaque = True

        self.hojaActual = 0

    def show_almanaque(self, screen):

        self.pila = pygame.image.load('graphics/elementos_graficos/marcoPila.png')
        self.pila = pygame.transform.scale(self.pila, (250,250))
        self.madera = pygame.image.load('graphics/elementos_graficos/marcoMadera.png')
        self.madera = pygame.transform.scale(self.madera, (250,250))
        self.cable = pygame.image.load('graphics/elementos_graficos/marcoCable.png')
        self.cable = pygame.transform.scale(self.cable, (250,250))
        self.cuerda = pygame.image.load('graphics/elementos_graficos/marcoCuerda.png')
        self.cuerda = pygame.transform.scale(self.cuerda, (250,250))

        self.fontsito = pygame.font.Font('graphics/font/pixelart.TTF', 20)  
        self.screen.fill((50,50,50))

        self.nib = self.fontsito.render(str(self.player.items_num[0]), True, (255, 255, 255))  # items bateria
        self.nic = self.fontsito.render(str(self.player.items_num[1]), True, (255, 255, 255))  # items madera
        self.nia = self.fontsito.render(str(self.player.items_num[2]), True, (255, 255, 255))  # items cable
        self.nim = self.fontsito.render(str(self.player.items_num[3]), True, (255, 255, 255))  # items cuerda

        cables_text = self.fontsito.render("Cable", True, "white") 
        cuerda_text = self.fontsito.render("Cuerda", True, "white") 
        madera_text = self.fontsito.render("Madera", True, "white") 
        pila_text = self.fontsito.render("Pila", True, "white") 

        boton=pygame.image.load("graphics/elementos_graficos/botonT.png")
        boton=pygame.transform.scale(boton,(50,50))
        
        imageButton = pygame.image.load("graphics/elementos_graficos/botonT.png")
        imageButton = pygame.transform.scale(imageButton, (35,35))
        imageButton = pygame.transform.flip(imageButton, True, False)

        self.buttonN = Button(imageButton, (screen.get_width()-imageButton.get_width()//2-10,screen.get_height()//2), "", pygame.font.Font("graphics/font/RobotoMono-VariableFont_wght.ttf", 12), (0,0,0), (0,0,0))

        
        self.buttonR = Button(imageButton, (imageButton.get_width()//2+10,screen.get_height()//2), "", pygame.font.Font("graphics/font/RobotoMono-VariableFont_wght.TTF", 12), (0,0,0), (0,0,0))
        self.popUp = None


        self.salir_botton = Button(image=boton, pos=(100,650), text_input="",font=self.fontsito,base_color="#4D4D5C",hovering_color="#75E2EC")

        self.timeCreate = time()

        self.enable = True
        
        while self.almanaque:

            self.screen.blit(self.cable, (50, 225))
            self.screen.blit(self.cuerda, (375, 225))
            self.screen.blit(self.madera, (675, 225))
            self.screen.blit(self.pila, (975, 225))

            self.screen.blit(cables_text, (140,200))
            self.screen.blit(cuerda_text, (460, 200))
            self.screen.blit(madera_text, (750,200))
            self.screen.blit(pila_text, (1075, 200))

            text_rect = self.nic.get_rect()
            text_rect.center = (50, 225)
            self.screen.blit(self.nic, text_rect)  # Dibuja el texto de cable en la pantalla
            text_rect = self.nia.get_rect()
            text_rect.center = (375, 225)
            self.screen.blit(self.nia, text_rect)  # Dibuja el texto de cuerda en la pantalla
            text_rect = self.nim.get_rect()
            text_rect.center = (675, 225)
            self.screen.blit(self.nim, text_rect)  # Dibuja el texto de madera en la pantalla
            text_rect = self.nib.get_rect()
            text_rect.center = (975, 225)
            self.screen.blit(self.nib, text_rect)  # Dibuja el texto de bateria en la pantalla

            self.salir_botton.cargar(self.screen)
            self.salir_botton.cambiar_color(pygame.mouse.get_pos())

            events = pygame.event.get()

            for event in events:
                #Salir
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.salir_botton.checkForInput(pygame.mouse.get_pos()):
                        self.almanaque = False
                        self.salir_botton.click(self.screen)
                        #self.musica_almanaque.stop() //Agregar
                        return self.almanaque
                
                pygame.display.update()
                    