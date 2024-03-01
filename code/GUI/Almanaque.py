import pygame

import numpy as np

from time import time

from GUI.PopUp import PopUp
from GUI.button import Button

class Almanaque():
    def __init__(self, screen, background, listaAnimales=None,rect=None, center=False):
        self.screen = screen
        if not center:
            self.rect = pygame.Rect(rect)
        else:
            self.rect = pygame.Rect(0,0,rect[0], rect[1])
            self.rect.center=(screen.get_width()//2, screen.get_height()//2)
            
        self.superficie = pygame.Surface((self.rect.width, self.rect.height))
        self.background = pygame.image.load(background)
        self.background = pygame.transform.scale(self.background,self.rect.size)

        self.fontsito = pygame.font.Font('Fonts/pixelart.TTF', 20)  

        self.hojaActual = 0

        self.listaAnimales = np.array(listaAnimales).copy()


        for animal in self.listaAnimales:
            animal.enable = False
            animal.direction = "SR"
        numAnimales = len(self.listaAnimales)

        self.pressed = False
        self.pressedAnt = False

        numHojas = int(numAnimales/6)
        if numAnimales/6>int(numAnimales/6):
            numHojas+=1
        
        self.hojas = np.empty((numHojas, 2, 3), dtype=object)
        self.hojas.fill(None)

        if self.listaAnimales is not None:
            for i, animal in enumerate(self.listaAnimales):
                columna = i%3
                fila = int((i/3)%2)
                hoja= int((i/6))

                animal.direction = "SR"
                animal.enable = False

                self.hojas[hoja][fila][columna] = animal

        self.ancho_parte = screen.get_width() // 4
        self.alto_parte = screen.get_height() // 2


        boton=pygame.image.load("Graficos/elementos_img/button.png")
        boton=pygame.transform.scale(boton,(240,90))


        imageButton = pygame.image.load("Graficos/elementos_img/botonT.png")
        imageButton = pygame.transform.scale(imageButton, (35,35))
        self.buttonN = Button(imageButton, (screen.get_width()-imageButton.get_width()//2-10,screen.get_height()//2), "", pygame.font.Font("Fonts/RobotoMono-VariableFont_wght.TTF", 12), (0,0,0), (0,0,0))

        imageButton = pygame.transform.flip(imageButton, True, False)
        self.buttonR = Button(imageButton, (imageButton.get_width()//2+10,screen.get_height()//2), "", pygame.font.Font("Fonts/RobotoMono-VariableFont_wght.TTF", 12), (0,0,0), (0,0,0))
        self.popUp = None


        self.salir_botton = Button(image=boton, pos=(400,515),text_input="Regresar",font=self.fontsito,base_color="#4D4D5C",hovering_color="#75E2EC")

        self.timeCreate = time()

        self.enable = True

    def update(self, events):
        self.pressed = pygame.mouse.get_pressed()[0]
            

            
        self.superficie.blit(self.background, (0,0))
        if len(self.hojas)>0:
            hoja = self.hojas[self.hojaActual]
            for i, fila in enumerate(hoja):
                for j, animal in enumerate(fila):
                    if animal is not None:
                        rect = animal.image.get_rect(center = ((j+1) * self.ancho_parte, self.alto_parte+ (-73 if i==0 else 73)))
                        rectFondo = animal.imageBackground.get_rect(center = ((j+1) * self.ancho_parte, self.alto_parte+ (-73 if i==0 else 73)))
                        self.superficie.blit(animal.imageBackground, rectFondo)
                        self.superficie.blit(animal.image, rect)
                        animal.etiqueta.set_position(rectFondo.centerx-animal.etiqueta.rect.width//2, rectFondo.bottom-animal.etiqueta.rect.height//2)
                        animal.etiqueta.update(self.superficie)

                        if animal.nuevo:
                            animal.etiquetaNew.set_position(rectFondo.centerx-animal.etiquetaNew.rect.width//2, rectFondo.top-animal.etiqueta.rect.height//2)
                            animal.etiquetaNew.update(self.superficie)

                        if  not self.pressedAnt and self.pressed:
                            if rectFondo.collidepoint(pygame.mouse.get_pos()) and (self.popUp is None or not self.popUp.enabled) and time()-self.timeCreate>0.5:
                                self.popUp = PopUp(self.screen, 300, 420, "Detalles", animal.image, nombreCien=animal.nombreCien, nombre=animal.nombre, descripcion=animal.descripcion, parametros=animal.parametros, tipo=animal.tipo, colorD=animal.colorDetalles, num_especies = animal.especimenes)
                                animal.nuevo = False
                                self.popUp.active()
                        # if rect.collidepoint(pygame.mouse.get_pos()):
                        #     print("hover")

        if(self.hojaActual<len(self.hojas)-1):
            self.buttonN.cargar(self.superficie)
        if(self.hojaActual>0):
            self.buttonR.cargar(self.superficie)

        self.salir_botton.cargar(self.superficie)
        self.salir_botton.cambiar_color(pygame.mouse.get_pos())

        self.screen.blit(self.superficie, self.rect)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and  (self.popUp is None or not self.popUp.enabled):
                if self.buttonN.checkForInput(pygame.mouse.get_pos()) and self.hojaActual<len(self.hojas)-1:
                    self.buttonN.click(self.screen)
                    self.hojaActual+=1
                if self.buttonR.checkForInput(pygame.mouse.get_pos()) and self.hojaActual>0:
                    self.hojaActual-=1
                    self.buttonR.click(self.screen)
                if self.salir_botton.checkForInput(pygame.mouse.get_pos()):
                        self.enable = False
        
            
        if self.popUp is not None:
            self.popUp.show(events) 

        for animal in self.listaAnimales:
            animal.update()

        self.pressedAnt = self.pressed