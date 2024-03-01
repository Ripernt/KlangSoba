import pygame

class GradientSurface:
    def __init__(self, width, height, color):
        self.width = width
        self.height = height
        self.color = color
        self.surface = None
        self.rect = None

        self.render()

    def render(self):
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.surface.fill((0,0,0,0))
        gradient = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        gradient.fill((0,0,0,0))
        start_alpha = self.color[3]
        end_alpha = 0

        for y in range(self.height):
            alpha = int(start_alpha - ((start_alpha - end_alpha) / self.height) * y)
            pygame.draw.line(gradient, (self.color[0], self.color[1], self.color[2], alpha), (0, y), (self.width, y))

        self.surface.blit(gradient, (0, 0))
        self.rect = self.surface.get_rect()

    def draw(self, surface, pos):
        self.rect.topleft = pos
        surface.blit(self.surface, self.rect)