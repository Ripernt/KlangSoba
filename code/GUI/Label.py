import pygame

class Label:
    def __init__(self, text, font_path, font_size, rect, text_color=(255, 255, 255), bg_color=None, align="left"):
        self.text = text
        self.font_path = font_path
        self.font_size = font_size
        self.text_color = text_color
        self.bg_color = bg_color
        self.align = align
        self.rect = pygame.Rect(rect)
        self.font = pygame.font.Font(self.font_path, self.font_size)
        self.rendered_text = None
        self.rendered_rect = None
        
        self.render_text()
    
    def render_text(self):
        self.rendered_text = self.font.render(self.text, True, self.text_color, self.bg_color)
        self.rendered_rect = self.rendered_text.get_rect()
        if self.align == "left":
            self.rendered_rect.left = self.rect.left
        elif self.align == "center":
            self.rendered_rect.centerx = self.rect.centerx
        elif self.align == "right":
            self.rendered_rect.right = self.rect.right
        self.rendered_rect.centery = self.rect.centery
    
    def set_text(self, text):
        self.text = text
        self.render_text()
        
    def set_bg_color(self, bg_color):
        self.bg_color = bg_color
        self.render_text()
    
    def set_text_color(self, text_color):
        self.text_color = text_color
        self.render_text()
    
    def set_align(self, align):
        self.align = align
        self.render_text()
    
    def set_rect(self, rect):
        self.rect = pygame.Rect(rect)
        self.render_text()
    def set_position(self,x,y):
        self.rect.x = x 
        self.rect.y = y 
        self.render_text()
        
    def update(self, surface):
        if self.bg_color is not None:
            pygame.draw.rect(surface, self.bg_color, self.rect)
        surface.blit(self.rendered_text, self.rendered_rect)
