import pygame

import numpy as np

from time import time

from GUI.PopUp import PopUp
from GUI.button import Button

class MenuControles():
    def __init__(self, screen, background,rect= None, center = False):
        
        self.screen = screen
        if not center:
            self.rect = pygame.Rect(rect)
        else:
            self.rect = pygame.Rect(0,0,rect[0], rect[1])
            self.rect.center=(screen.get_width()//2, screen.get_height()//2)
            
        self.superficie = pygame.Surface((self.rect.width, self.rect.height))
        self.background = pygame.image.load(background)
        self.background = pygame.transform.scale(self.background,self.rect.size)

        self.menucontroles = True

        self.hojaActual = 0

    def show_menu_controles(self, screen):

        self.fontsito = pygame.font.Font('graphics/font/pixelart.TTF', 20)  
        self.screen.fill((50,50,50))

        boton=pygame.image.load("graphics/elementos_graficos/botonT.png")
        boton=pygame.transform.scale(boton,(50,50))
        
        imageButton = pygame.image.load("graphics/elementos_graficos/botonT.png")
        imageButton = pygame.transform.scale(imageButton, (35,35))
        imageButton = pygame.transform.flip(imageButton, True, False)

        controles = pygame.image.load("graphics/elementos_graficos/menuControles.png")
        controles = pygame.transform.scale(controles,(1280,670))

        self.buttonN = Button(imageButton, (screen.get_width()-imageButton.get_width()//2-10,screen.get_height()//2), "", pygame.font.Font("graphics/font/RobotoMono-VariableFont_wght.ttf", 12), (0,0,0), (0,0,0))
        
        self.buttonR = Button(imageButton, (imageButton.get_width()//2+10,screen.get_height()//2), "", pygame.font.Font("graphics/font/RobotoMono-VariableFont_wght.TTF", 12), (0,0,0), (0,0,0))
        self.popUp = None


        self.salir_botton = Button(image=boton, pos=(100,690), text_input="",font=self.fontsito,base_color="#4D4D5C",hovering_color="#75E2EC")

        self.timeCreate = time()

        self.enable = True
        
        while self.menucontroles:
            self.salir_botton.cargar(self.screen)
            self.salir_botton.cambiar_color(pygame.mouse.get_pos())
            self.screen.blit(controles,(0,0))
            events = pygame.event.get()

            for event in events:
                #Salir
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.salir_botton.checkForInput(pygame.mouse.get_pos()):
                        self.menucontroles = False
                        self.salir_botton.click(self.screen)
                        
                        return self.menucontroles
                
                pygame.display.update()