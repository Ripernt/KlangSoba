import pygame
from time import time
from random import randint
import webbrowser


class Button():

    def __init__(self,image,pos,text_input,font,base_color,hovering_color, Sonido_Precionar='audio/death.wav', link = None):

        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color= base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)

        if self.image is None:
            self.image = self.text

        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos-8))

        self.hovering = False
        self.hoveringAnt = False

        self.efectoTimeInit = 0

        self.efectoTime = 0.2

        self.Button_sound = pygame.mixer.Sound(Sonido_Precionar)

        self.link = link

    def parpadeo(self):
        par = bool(randint(0, 1))

        if par:
            self.text = self.font.render(self.text_input,True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input,True,self.base_color)

    def cargar(self,screen):
        if self.image is not None:
            screen.blit(self.image,self.rect)
        screen.blit(self.text,self.text_rect)

        if self.hovering and not self.hoveringAnt:
            self.efectoTimeInit = time()
            
        elif not self.hovering and self.hoveringAnt:
            self.text = self.font.render(self.text_input,True,self.base_color)

        if self.hovering and self.hoveringAnt:
            if time()-self.efectoTimeInit<self.efectoTime:
                self.parpadeo()
            else:
                self.text = self.font.render(self.text_input,True, self.hovering_color)
        
        self.hoveringAnt = self.hovering
        
    def checkForInput(self,position):

        if position[0] in range(self.rect.left,self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):

            return True
        
    def click(self,screen):
        # Simular efecto de hundimiento
        self.Button_sound.set_volume(0.4)
        self.Button_sound.play()
        
        self.rect.move_ip(0, 5)
        self.cargar(screen)
        pygame.display.flip()
        pygame.time.wait(50)
        self.rect.move_ip(0, -5)
        self.cargar(screen)
        pygame.display.flip()

        if self.link:
            webbrowser.open(self.link)
        

    def cambiar_color(self,position):

        if position[0] in range(self.rect.left,self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.hovering = True

        else:
            self.hovering = False

