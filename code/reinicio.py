import pygame, sys, threading
from spritesheet_functions import SpriteSheet
from settings import *
from GUI.MenuInstrumentos import MInstrumentos
from math import sqrt, pow
from level import Level, Level_2

def eucDis(p1, p2): 
    difx = p1[0]-p2[0]
    dify = p1[1]-p2[1]
    
    dis = sqrt(pow(difx,2)+pow(dify,2))
    
    return dis

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

        print("inicializando niveles")
        self.downloaded_level.append(Level())
        print("primer nivel...")
        self.downloaded_level.append(Level_2(self.downloaded_level[0].player))
        print("segundo nivel...")
        
        self.level = self.downloaded_level[0]
        
        self.player = self.level.player
        
        print("level hecho")

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

    def run(self):
        from GUI.Pausa import PausaMenu
        print("Run")
        self.main_sound.music.play(-1)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.cursor.close()
                    self.conexion.close()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.level.toggle_menu()
                    if event.key == pygame.K_ESCAPE:
                        self.main_sound.music.pause()
                        self.musica_personalizada.play(1)
                        self.Pausita = PausaMenu(self.main_sound,self.musica_personalizada)
                        xd = self.Pausita.show_menu()
                        if xd == False:
                            self.main_sound.music.unpause()
                    if event.key == pygame.K_m:
                        self.main_sound.music.pause()
                        self.musica_instrumentos.play(-1)
                        self.Instrumentos = MInstrumentos(self.main_sound,self.musica_instrumentos)#Cambiar la musica
                        hola = self.Instrumentos.mostrar_instrumentos()
                        if hola == False:
                            self.main_sound.music.unpause()

            self.screen.fill(WATER_COLOR)
            self.level.run()
            
            if(eucDis(self.player.rect.topleft, (3743, 670))<70 and self.currentLevelNum != 1):
                print("que sucede chaval")
                self.currentLevelNum = 1
                self.level = self.downloaded_level[self.currentLevelNum]
                self.level.resetPlayer()
            if(eucDis(self.player.rect.topleft, (827, 1197))<70 and self.currentLevelNum != 0):
                print("que sucede chaval")
                self.currentLevelNum = 0
                self.level = self.downloaded_level[self.currentLevelNum]
                self.level.resetPlayer()
                
            pygame.display.update()
            self.clock.tick(FPS)
            
            pygame.display.set_caption(f'fps: {round(self.clock.get_fps())}')

    def ReiniciarNivel(self):
        print("Reiniciando el nivel")
        threadReLevel = threading.Thread(target= self.CargarNivel)
        threadReLevel.start()
        threadReCargaNivel = threading.Thread(target= self.ReCargarNivel)
        threadReCargaNivel.start()
        self.Animacion_Carga()
        threadReLevel.join()
        self.run()