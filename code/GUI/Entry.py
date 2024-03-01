import pygame as pg

class InputBox:

    def __init__(self, rect, textSec='', colorValue=[(255,255,255), (255,255,255)], font = None):
        self.rect = pg.Rect(rect)
        self.wMin = rect[2]
        self.colorValue = colorValue
        self.textSec = textSec
        self.text = textSec
        if font is None:
            self.font = pg.font.Font("graphics/font/pixelart.TTF", int(rect[3]*0.55))
            # self.font.set_bold(True)
        else:
            self.font = font
        self.txt_surface = self.font.render(self.text, True, self.colorValue[0])
        self.active = False


        self.blink_interval = 500  # Intervalo de tiempo del cursor en milisegundos
        self.blink_timer = 0
        self.show_cursor = False

    def setText(self, text):
        self.text = text
        self.txt_surface = self.font.render(self.text, True, self.colorValue[0])
    def getText(self):
        if self.text == self.textSec:
            return ""
        else:
            return self.text
    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = True
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.colorValue[1] if self.active else self.colorValue[1]
        if event.type == pg.KEYDOWN:
            if self.active:
                
                if event.key == pg.K_RETURN:
                    self.active = False
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.colorValue[0])
        if not self.active:
            if self.text == '' or self.text == self.textSec:
                self.text = self.textSec
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, (140,140,140))
        else:
            if self.text == self.textSec:
                self.text = ''
            # Re-render the text.
            self.txt_surface = self.font.render(self.text, True, self.colorValue[0])

                

    def update(self, window):
        # Resize the box if the text is too long.
        width = max(self.wMin, self.txt_surface.get_width()+10)
        self.rect.w = width


        # Añadir un temporizador para el cursor
        self.blink_timer += 18
        if self.blink_timer >= self.blink_interval:
            self.blink_timer %= self.blink_interval
            self.show_cursor = not self.show_cursor

        self.draw(window)
        # Añadir el cursor al texto si la InputBox está activa
        if self.active:
            cursor_pos = self.font.size(self.text[:])[0]
            cursor_height = self.font.size(self.text)[1]
            if self.show_cursor:
                pg.draw.line(window, (0, 0, 0), (self.rect.x + cursor_pos + 6, self.rect.y + 8),
                                (self.rect.x + cursor_pos + 6, self.rect.y + self.rect.height - 8), 2)


    def draw(self, screen):
        # Blit the rect.
        pg.draw.rect(screen, (255,255,255), self.rect)
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))