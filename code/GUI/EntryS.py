import pygame
import sys
class Entry():
    def __init__(self, screen, position, digitos, colorBorder = (0,0,0), color = (200,200,200), size=20, espacio=5, borderR=5):
        self.screen = screen
        self.position = position
        self.digitos = digitos
        self.size = size
        self.espacio = espacio

        self.surface = pygame.Surface((size*digitos+espacio*(digitos-1), size)).convert_alpha()
        self.surface.fill((0,0,0,0))
        self.rect = pygame.Rect(position[0]-self.surface.get_width()//2, position[1]-size//2, self.surface.get_width(), self.surface.get_height())
        self.rectDig = pygame.Rect(0,0, size, size)
        for i in range(digitos):
            pygame.draw.rect(self.surface,color, self.rectDig,0, borderR)
            pygame.draw.rect(self.surface,colorBorder, self.rectDig, 1, borderR)
            self.rectDig.x+=size+espacio
        self.data = ""
        self.foco = False

        self.cursorA = False
        self.cursorT = 0

        self.surfaceC = self.surface.copy()

        self.font = pygame.font.Font("graphics/font/joystix.ttf", 20)


    def update(self, events):
        mouseP = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(mouseP):
                    self.foco = True
                else:
                    self.foco = False
            if event.type == pygame.KEYDOWN:

                key_name = pygame.key.name(event.key)
                if key_name.isdigit() and self.foco:
                    if len(self.data)<self.digitos:
                        self.data+=event.unicode
                        self.cursorA = True
                        self.cursorT=pygame.time.get_ticks()
                if event.key == pygame.K_BACKSPACE:
                    self.data = self.data[:-1] 
                    self.cursorA = True
                    self.cursorT=pygame.time.get_ticks()
                if event.key == pygame.K_RETURN:
                    print(self.data)





        self.surfaceC.blit(self.surface, (0,0))
        if self.foco:
            if pygame.time.get_ticks()-self.cursorT>500:
                self.cursorT = pygame.time.get_ticks()
                self.cursorA=not self.cursorA
            if self.cursorA:
                x = len(self.data)*(self.size*1+self.espacio)+self.size//2
                pygame.draw.line(self.surfaceC, (0,0,0), (x, 10), (x, self.size-10),3)
        for i in range(len(self.data)):
            render = self.font.render(self.data[i:i+1], True, (0,0,0))
            x = i*(self.size*1+self.espacio)+self.size//2
            renderRect = render.get_rect(center=(x,self.size//2+3))
            self.surfaceC.blit(render, renderRect)
        self.screen.blit(self.surfaceC, self.rect)



