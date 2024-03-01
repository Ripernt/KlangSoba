import pygame

class Parrafo:
    def __init__(self, text, font, color, width=None):
        self.text = text
        self.font = font
        self.color = color
        self.width = width
        self.lines = []
        self.surface = None
        self.render()

    def render(self):
        self.lines = []
        words = self.text.split()
        if self.width:
            self.wrap_text(words)
        else:
            self.lines.append(" ".join(words))
        line_height = self.font.size("Tg")[1]
        self.surface = pygame.Surface((self.width, line_height * len(self.lines)), pygame.SRCALPHA)
        y = 0
        for line in self.lines:
            surface = self.font.render(line, False, self.color)
            self.surface.blit(surface, (0, y))
            y += line_height

    def wrap_text(self, words):
        line = []
        for word in words:
            if self.font.size(" ".join(line + [word]))[0] > self.width:
                self.lines.append(" ".join(line))
                line = [word]
            else:
                line.append(word)
        if line:
            self.lines.append(" ".join(line))
