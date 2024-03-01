import pygame, sys, threading

from level import Level 
from time import time
from settings import *
from inicio import Inicio
from GUI.Pausa import PausaMenu
from GUI.button import Button
from GUI.Entry import InputBox
from spritesheet_functions import SpriteSheet
from tkinter import messagebox


class Game:
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('me la soba')
        self.Inicio = Inicio()
        #self.cifrado = Cifradito()
        self.progreso = 0	
        self.fontsito = pygame.font.Font('graphics/font/joystix.ttf', 20) 
        
    """def conectarBase(self):
        try: 
            self.conexion = Conectar.conectar()
            self.cursor = self.conexion.cursor()
            print("conectado")
        except mysql.connector.Error as error:
                print("Se produjo un error al conectar a la base de datos: {}".format(error))"""

    def iniciarSesion(self):
        pygame.display.update()

        self.screen.fill((50, 50, 50))

        menu_text = self.fontsito.render("Inicia Sesion con tu Fast-Stern ID", True, "white")
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/10))

        fondo = pygame.image.load("graphics/elementos_graficos/fondosgenerico.png")

        fondo = pygame.transform.scale(fondo, (SCREEN_WIDTH, SCREEN_HEIGHT))

        botoniniciar = Button(image=generalButton, pos=(SCREEN_WIDTH/2,500),text_input="Iniciar Sesion",font=self.fontsito,base_color="#4D4D5C",hovering_color="#75E2EC")

        cajaI = InputBox((200,200,400,32), "Correo", colorValue=[(0,0,0), (255,0,0)])
        cajaC = InputBox((200,300,400,32), "Contraseña", colorValue=[(0,0,0), (255,0,0)])

        botoniniciar.cargar(self.screen)
        botoniniciar.cambiar_color(pygame.mouse.get_pos())
        #renderT = None

        """while True:
            self.screen.blit(fondo, (0,0))

            self.screen.blit(menu_text, menu_rect)
            
            if renderT is not None:
                self.screen.blit(renderT, rect)




            cajaI.update(self.screen)
            cajaC.update(self.screen)

            for event in pygame.event.get():
                cajaI.handle_event(event)
                cajaC.handle_event(event)

                if event.type == pygame.QUIT:
                    respuesta = messagebox.askyesno("Precaución", "Se perderan los avances de este nivel. ¿Estás seguro?")
                    if respuesta:
                        # Acción a realizar si se confirma
                        print("Confirmado")
                        self.cursor.close()
                        self.conexion.close()
                        pygame.quit()
                        sys.exit()
                    else:
                        # Acción a realizar si se cancela
                        print("Cancelado") 

               if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.Pantalla_incio()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if botoniniciar.checkForInput(pygame.mouse.get_pos()):
                        botoniniciar.click(self.screen)
                        correo = cajaI.text
                        contraseña = cajaC.text
                        xd = self.cifrado.encriptado(contraseña)
                        t1 = threading.Thread(target= validar.validar,args=(correo,xd,self.cursor,self.conexion))
                        t1.start()
                        t1.join()
                        response = validar.responseI()
                        if isinstance(response, Sesion):
                            return response
                        else:
                            print(response)
                            textR = pygame.font.Font("graphics/font/joystix.ttf", 15)
                            renderT = textR.render(response, True, (255,0,0))
                            rect = renderT.get_rect(center=(SCREEN_WIDTH//2, 400))
                
            pygame.display.update()"""

    """def Registrarse(self):
        pygame.display.update()

        menu_text = self.fontsito.render("Inicia Sesion con tu Fast-Stern ID", True, "white")
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/10))


        fondo = pygame.image.load("graphics/elementos_graficos/fondosgenerico.png")

        fondo = pygame.transform.scale(fondo, (SCREEN_WIDTH, SCREEN_HEIGHT))

        botonregistrar = Button(image=generalButton, pos=(SCREEN_WIDTH/2,500),text_input="Registrar Usuario",font=self.fontsito,base_color="#4D4D5C",hovering_color="#75E2EC")
        
        caja = InputBox((SCREEN_WIDTH/2,100,400,32), "Nombre de usuario", colorValue=[(0,0,0), (255,0,0)]) 
        caja2 = InputBox((SCREEN_WIDTH/2,175,400,32), "Correo", colorValue=[(0,0,0), (255,0,0)]) 
        caja3 = InputBox((SCREEN_WIDTH/2,250,400,32), "contraseña", colorValue=[(0,0,0), (255,0,0)]) 
        caja4 = InputBox((SCREEN_WIDTH/2,325,400,32), "confirmacion", colorValue=[(0,0,0), (255,0,0)]) 

        renderT = None


        while True:
            self.screen.blit(fondo, (0,0))

            self.screen.blit(menu_text, menu_rect)

            botonregistrar.cargar(self.screen)
            botonregistrar.cambiar_color(pygame.mouse.get_pos())

            caja.update(self.screen)
            caja2.update(self.screen)
            caja3.update(self.screen)
            caja4.update(self.screen)

            if renderT is not None:
                self.screen.blit(renderT, rect)

            for event in pygame.event.get():
                caja.handle_event(event)
                caja2.handle_event(event)
                caja3.handle_event(event)
                caja4.handle_event(event)
                if event.type == pygame.QUIT:
                    respuesta = messagebox.askyesno("Precaución", "Se perderan los avances de este nivel. ¿Estás seguro?")
                    if respuesta:
                        # Acción a realizar si se confirma
                        print("Confirmado")
                        self.cursor.close()
                        self.conexion.close()
                        pygame.quit()
                        sys.exit()
                    else:
                        # Acción a realizar si se cancela
                        print("Cancelado")   

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.Pantalla_incio()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if botonregistrar.checkForInput(pygame.mouse.get_pos()):
                        botonregistrar.click(self.screen)
                        usuario = caja.getText()
                        correo = caja2.getText()
                        contraseña = caja3.getText()
                        confirmcontra = caja4.getText()
                        #renderT = None
                        
                        response = validar.validarRegistro(usuario,correo,contraseña,confirmcontra, self.conexion, self.cursor)
                        if response == "OK":
                            return
                        else:
                            
                            textR = pygame.font.Font("graphics/font/joystix.ttf", 15)
                            renderT = textR.render(response, True, (255,0,0))
                            rect = renderT.get_rect(center=(SCREEN_WIDTH//2, 430))      
            pygame.display.update()"""

    def CargarKS(self):
        print("Cargando")
        self.progreso = 20
        #print(self.progreso)
        self.clock = pygame.time.Clock()
        self.progreso = 30
        #main audio// Musica predetermijnada
        self.main_sound = pygame.mixer
        self.main_sound.music.load('audio/Monkberry Moon Delight.ogg')
        
        self.progreso = 50
        #pause audio//Musica personalizada
        self.musica_personalizada = pygame.mixer.Sound("audio/bass-loops-006-with-drums-long-loop-120-bpm-6111.mp3")
        #DB
        #print(self.progreso)       
        self.progreso = 503

    def mostrar_animacion_carga(self):
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

    def logos(self):
        print("mostrando logos")
        self.Inicio.logos()
        
    def inicializar_level(self):
        print("inicializando nivel")
        self.level = Level()
        print("level hecho")

    def Pantalla_incio(self):
        print("Mostrar pantalla de inicio")
        self.RoI = self.Inicio.inicio()
        if self.RoI:
            res = self.iniciarSesion()
            if res is not None:
                return res
        else:
            self.Registrarse()
            
    def run(self):
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

            self.screen.fill(WATER_COLOR)
            self.level.run()
            
            pygame.display.update()
            self.clock.tick(FPS)
    
    def iniciar_Juego(self):
            print("inicializar juego")
            threadLevel = threading.Thread(target=self.inicializar_level)
            threadLevel.start()
            self.logos()
            #threadConectar = threading.Thread(target=game.conectarBase)
            #threadConectar.start()
            sesion = self.Pantalla_incio()
            threadCargarKS = threading.Thread(target=self.CargarKS)
            threadCargarKS.start()
            self.mostrar_animacion_carga()
            threadLevel.join()
            self.run()