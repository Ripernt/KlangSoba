import pygame

class SeccionesTexto:
    def __init__(self, color, textos, size):
        self.color = color
        self.textos = textos
        self.size = size
        self.surface = None
        self.rect = None
        self.font = pygame.font.Font(None, 15)
        self.font2 = pygame.font.Font(None, 19)
        self.font2.set_bold(True)
        self.render()

    def render(self):
        width = self.size[0]
        height = self.size[1]
        padding = 10

        section_width = (width - padding * 4) // 3
        section_height = height - padding * 2

        self.surface = pygame.Surface((width, height))
        self.surface.fill(self.color)

        sep = self.size[0]//3


        for i in range(3):
            section_x = padding + i * (section_width + padding)
            section_rect = pygame.Rect(section_x, padding, section_width, section_height)
            


            line1 = self.font2.render(self.textos[i * 2], True, (255, 255, 255))
            line2 = self.font.render(self.textos[i * 2 + 1], True, (255, 255, 255))

            line1_rect = line1.get_rect(center=section_rect.center)
            line1_rect.top -= 15

            line2_rect = line2.get_rect(center=section_rect.center)
            line2_rect.top += 15

            self.surface.blit(line1, line1_rect)
            self.surface.blit(line2, line2_rect)

            pygame.draw.line(self.surface, (self.color[0]-20 if self.color[0]-20>0 else 0,  self.color[1]-20 if self.color[1]-20>0 else 0,  self.color[2]-20 if self.color[2]-20>0 else 0), (sep*(i+1), 0), (sep*(i+1), self.size[1]), 1)

        self.rect = self.surface.get_rect()

    def draw(self, surface, pos):
        self.rect.topleft = pos
        surface.blit(self.surface, self.rect)
