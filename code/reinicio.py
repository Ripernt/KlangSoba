import pygame,sys
from spritesheet_functions import SpriteSheet
from settings import *


class Reinicio():

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.progreso = 0

    def ReCargarNivel(self):
        print("Reiniciando el nivel")
        self.clock = pygame.time.Clock()
        self.progreso = 20
        self.progreso = 30
        self.main_sound = pygame.mixer
        self.main_sound.music.load('audio/Monkberry Moon Delight.ogg')
        self.progreso = 50
        self.musica_personalizada = pygame.mixer.Sound("audio/bass-loops-006-with-drums-long-loop-120-bpm-6111.mp3")
        self.progreso = 503

    def CargarNivel(self):
        from level import Level
        self.level = Level()

    def Animacion_Carga(self):
        print("Mostrar animación")
        bar_x = SCREEN_WIDTH//2-150
        bar_y = 350
        bar_width = 300
        bar_height = 20
        WHITE = (255, 255, 255)
        progress = 0
        animacion = []
        sprite_sheet = SpriteSheet("graphics/pantalla de carga/cargapotcat.png")
        sprite_sheet.scaled_sprite(3/10)
        
        w,h = sprite_sheet.getSize()
        wS = w//4
        for i in range(4):
            image = sprite_sheet.get_image(i*wS, 0, wS, h)
            animacion.append(image)
        pygame.mixer.music.stop()
        fontsito = pygame.font.SysFont("Bauhaus 93", 32) 
        superficie = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
        while progress<500:
            if progress < self.progreso and pygame.time.get_ticks()%5==0:
                progress += (self.progreso-progress)*0.2
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            superficie.fill((0,0,0))
            
            pygame.draw.rect(superficie, WHITE, [bar_x, bar_y, bar_width, bar_height], 2)
            pygame.draw.rect(superficie, WHITE, [bar_x, bar_y, bar_width * (progress / 500), bar_height])
            menu_text = fontsito.render(str(int(progress/500*100))+"%", True, "white")
            menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/6*4))
            superficie.blit(menu_text, menu_rect)
            superficie.blit(animacion[(pygame.time.get_ticks()//150)%4], (SCREEN_WIDTH//2-wS//2,200))
            self.screen.blit(superficie, (0,0))
            pygame.display.update()
        for i in range(255,-1, -1):
            superficie.set_alpha(i)
            self.screen.fill((0,0,0))
            self.screen.blit(superficie, (0,0))
            pygame.display.update()
            pygame.time.delay(1)
        pygame.time.delay(200)


