import pygame
import pygame.gfxdraw

class Range():
    def __init__(self, rect, texto):
        self.rect = pygame.Rect(rect)
        self.rect.x-=self.rect.width//2
        self.rect.y-=self.rect.height//2
        self.surface = pygame.Surface(self.rect.size)

        # va de 0 a 10
        self.range = 4

        self._down = False
        self._pointDrag = None
        self._initDrag = None

        self.font = pygame.font.Font("graphics/font/joystix.ttf", 18)

        self.renderT = self.font.render(texto, True, (255,255,255))
        self.rectText = self.renderT.get_rect(center=(900,rect[1]+32))
    def draw(self,screen, events):
        self._pointDrag=pygame.mouse.get_pos()
        for event in events:
            if event.type==pygame.MOUSEBUTTONDOWN:
                self._down = True
                self._initDrag = self._pointDrag
            if event.type==pygame.MOUSEBUTTONUP:
                self._down = False

            
            
        rectR = pygame.Rect(self.rect)
        rectR.height = 5
        rectR.width -=10 
        rectR.center = self.rect.center
        rectR.width = rectR.width/11*self.range
        pygame.draw.rect(screen, (255,255,255), rectR)
        pygame.draw.rect(screen, (255,255,255), self.rect, 1, 3)
        
        pygame.gfxdraw.aacircle(screen, rectR.right+8,rectR.centery,8,(255,255,255))
        pygame.gfxdraw.filled_circle(screen, rectR.right+8, rectR.centery, 8, (255,255,255))

        screen.blit(self.renderT, self.rectText)

        if self._down:
            if self.rect.collidepoint(self._initDrag):
                self.range = (self._pointDrag[0]-rectR.x-8)/(self.rect.width-10)*11
                if self.range<0:
                    self.range = 0
                if self.range>10:
                    self.range = 10