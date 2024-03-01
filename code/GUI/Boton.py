import pygame
import time
import threading
import math

def ease_out(t, tiempoEnd):
    return 1 - (1 - (t/(tiempoEnd/1000))) ** 2


class Boton:
    def __init__(self, rect, text, colorValue=[(0,0,0), (0,0,0)], text_color=(0, 0, 0), font=None, alpha=255):
        self.rect = pygame.Rect(rect[0], rect[1], rect[2], rect[3])
        self.text = text
        self.color = (255,255,255)
        self.text_color = text_color
        self.alpha = alpha

        self.colorValue = colorValue
        if font is None:
            self.font = pygame.font.Font("Fonts/ARCADECLASSIC.ttf", int(rect[3]*0.7))
            self.font.set_bold(True)
        else:
            self.font = font
        
        self._detect = False
        self._detectAnt = False

        self.pressed = False

        self.colorHover = None
        self.millis = None

        self.timeInit = None 
        self._cR = colorValue[0][0]
        self._cG = colorValue[0][1]
        self._cB = colorValue[0][2]

        self.hovering = True


        self.enabled = True

    def update(self, surface, event_list):
        # Dibuja el rectángulo del botón
        button_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA).convert_alpha()
        button_surf.fill((0,0,0,0))
        # pygame.draw.rect(button_surf, (self._cR,self._cG,self._cB), button_surf.get_rect(), border_radius=0)
        if self.enabled: 
            button_surf.set_alpha(self.alpha)
        else:
            button_surf.set_alpha(125)
        surface.blit(button_surf, self.rect)

        # Dibuja el texto centrado en el botón
        text_surf = self.font.render(self.text, True, self.text_color)

        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

        if self.enabled:
            if self.hover(event_list):
                self.setTransition(self.colorValue[1], 200)
                self.startTransition()
            else:
                self.setTransition(self.colorValue[0], 200)
                self.startTransition()


    def hover(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEMOTION:
                if self.rect.collidepoint(event.pos):
                    self.hovering = True
                else:
                    self.hovering = False

        return self.hovering

    def setTransition(self, colorHover, millis):
        if self.timeInit is None:
            self.colorHover = colorHover
            self.millis = millis

    def startTransition(self):
        if self.timeInit is None and self.color != self.colorHover:
            self.timeInit = time.time()
            t = threading.Thread(target=self.transitionsApply, args=())
            t.start()

    def transitionsApply(self):
        while(True):
            # Codifo para las transiciones de color
            if self.timeInit is not None and time.time()-self.timeInit<(self.millis)/1000:
                r = ease_out(time.time()-self.timeInit, self.millis)
                self._cR = self.color[0]+r*(self.colorHover[0]-self.color[0])
                self._cG = self.color[1]+r*(self.colorHover[1]-self.color[1])
                self._cB = self.color[2]+r*(self.colorHover[2]-self.color[2])
            else:
                break
        self.timeInit = None
        self.color = (int(round(self._cR)), int(round(self._cG)), int(round(self._cB)))


    def is_clicked(self, event_list):
        if not self.enabled:
            return False
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self._detect = True
            if self._detect and event.type != pygame.MOUSEBUTTONUP and not self.pressed:
                self.pressed = True
                return True
            elif event.type == pygame.MOUSEBUTTONUP:
                self._detect = False
                self.pressed = False
                return False





