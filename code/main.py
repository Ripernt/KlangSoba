import pygame, sys, threading
from time import time
from settings import *
from level import *
from inicio import Inicio
from DB import conectar as Conectar
from DB.conectar import *
from DB import validar
from DB.Sesion  import Sesion
from GUI.Pausa import PausaMenu
from GUI.button import Button
from GUI.Entry import InputBox
from GUI.MenuInstrumentos import MInstrumentos
from Npc import *
#from secure.cifrado import Cifradito
from spritesheet_functions import SpriteSheet
from tkinter import messagebox
from math import sqrt, pow
from Npc import * 

def eucDis(p1, p2): 
    difx = p1[0]-p2[0]
    dify = p1[1]-p2[1]
    
    dis = sqrt(pow(difx,2)+pow(dify,2))
    
    return dis

class Game:
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('KlangSoba')
        self.Inicio = Inicio()
        #self.cifrado = Cifradito()
        self.progreso = 0	
        self.fontsito = pygame.font.Font('graphics/font/joystix.ttf', 20) 
        
        self.color_level = [WATER_COLOR, (38, 11, 45)]
        
        self.downloaded_level = []
        self.level = None
        
        self.player = None
        
        self.currentLevelNum = 0
        
        
    def conectarBase(self):
        try: 
            print("Conexion, cursor")
            self.conexion = Conectar.conectar()
            self.cursor = self.conexion.cursor()
            print("conectado")
        except mysql.connector.Error as error:
                print("Se encontro un error al conectar a la base de datos: {}".format(error))

    def iniciarSesion(self):
        global lista
        pygame.display.update()

        self.screen.fill((50, 50, 50))

        menu_text = self.fontsito.render("Inicia Sesion con tu Fast-Stern ID", True, "white")
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/10))

        fondo = pygame.image.load("graphics/elementos_graficos/fondosgenerico.png")

        fondo = pygame.transform.scale(fondo, (SCREEN_WIDTH, SCREEN_HEIGHT))

        botoniniciar = Button(image=generalButton, pos=(SCREEN_WIDTH/2,500),text_input="Iniciar Sesion",font=self.fontsito,base_color="#4D4D5C",hovering_color="#75E2EC")
        botonRegresarInicio = Button(image=botonRegresar, pos=(150,500), text_input="", font=self.fontsito, base_color="#4D4D5C",hovering_color="#75E2EC")

        cajaI = InputBox((SCREEN_WIDTH/3,200,400,32), "Correo", colorValue=[(0,0,0), (255,0,0)])
        cajaC = InputBox((SCREEN_WIDTH/3,300,400,32), "", colorValue=[(0,0,0), (255,0,0)], hidden = True)

        renderT = None

        while True:
            self.screen.blit(fondo, (0,0))

            self.screen.blit(menu_text, menu_rect)
            
            if renderT is not None:
                self.screen.blit(renderT, rect)

            botoniniciar.cargar(self.screen)
            botoniniciar.cambiar_color(pygame.mouse.get_pos())

            botonRegresarInicio.cargar(self.screen)
            botonRegresarInicio.cambiar_color(pygame.mouse.get_pos())

            cajaI.update(self.screen)
            cajaC.update(self.screen)

            for event in pygame.event.get():
                cajaI.handle_event(event)
                cajaC.handle_event(event)

                if event.type == pygame.QUIT:
                    respuesta = messagebox.askyesno("Precaución", "Se perderan los avances de este nivel. ¿Estás seguro?")
                    if respuesta:
                        
                        print("Confirmado")
                        self.cursor.close()
                        self.conexion.close()
                        pygame.quit()
                        sys.exit()
                    else:
                        
                        print("Cancelado") 

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        botonRegresarInicio.click(self.screen)
                        self.Pantalla_incio()
                        
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if botonRegresarInicio.checkForInput(pygame.mouse.get_pos()):
                        botonRegresarInicio.click(self.screen)
                        self.Pantalla_incio()
                    if botoniniciar.checkForInput(pygame.mouse.get_pos()):
                        botoniniciar.click(self.screen)
                        correo = cajaI.text
                        contraseña = cajaC.text
                        #xd = self.cifrado.encriptado(contraseña)
                        t1 = threading.Thread(target= validar.validar,args=(correo,contraseña,self.cursor,self.conexion)) #,xd,
                        t1.start()
                        t1.join()
                        response = validar.responseI()

                        if isinstance(response, Sesion):
                            
                            lista = Item.valor(self)
                            re = validar.obtener_items(correo,self.conexion, self.cursor)
                            lista = re 
                            Item.carga_items(self,lista)
                            
                            instrumento = validar.obtener_instrumento_piano(correo,self.conexion,self.cursor)
                            print(instrumento)
                            MInstrumentos.carga_instrumento(self,instrumento)
                            return response

                        else:
                            print(response)
                            textR = pygame.font.Font("graphics/font/joystix.ttf", 15)
                            renderT = textR.render(response, True, (255,0,0))
                            rect = renderT.get_rect(center=(SCREEN_WIDTH//2, 400))
                    
            pygame.display.update()
    def mandar_lista():
        return lista
    def Registrarse(self):
        pygame.display.update()

        menu_text = self.fontsito.render("Inicia Sesion con tu Fast-Stern ID", True, "white")
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/10))


        fondo = pygame.image.load("graphics/elementos_graficos/fondosgenerico.png")

        fondo = pygame.transform.scale(fondo, (SCREEN_WIDTH, SCREEN_HEIGHT))

        botonregistrar = Button(image=generalButton, pos=(SCREEN_WIDTH/2,500),text_input="Registrar Usuario",font=self.fontsito,base_color="#4D4D5C",hovering_color="#75E2EC")
        botonRegresarRegistro = Button(image=botonRegresar, pos=(150,500),text_input="",font=self.fontsito,base_color="#4D4D5C",hovering_color="#75E2EC")

        caja = InputBox((SCREEN_WIDTH/3,100,400,32), "Nombre de usuario", colorValue=[(0,0,0), (255,0,0)]) 
        caja2 = InputBox((SCREEN_WIDTH/3,175,400,32), "Correo", colorValue=[(0,0,0), (255,0,0)]) 
        caja3 = InputBox((SCREEN_WIDTH/3,250,400,32), "", colorValue=[(0,0,0), (255,0,0)], hidden = True) 
        caja4 = InputBox((SCREEN_WIDTH/3,325,400,32), "confirmacion", colorValue=[(0,0,0), (255,0,0)], hidden= True) 

        renderT = None


        while True:
            self.screen.blit(fondo, (0,0))

            self.screen.blit(menu_text, menu_rect)

            botonregistrar.cargar(self.screen)
            botonregistrar.cambiar_color(pygame.mouse.get_pos())

            botonRegresarRegistro.cargar(self.screen)
            botonRegresarRegistro.cambiar_color(pygame.mouse.get_pos())

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
                        botonRegresarRegistro.click(self.screen)
                        self.Pantalla_incio()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if botonRegresarRegistro.checkForInput(pygame.mouse.get_pos()):
                        botonRegresarRegistro.click(self.screen)
                        self.Pantalla_incio()

                    if botonregistrar.checkForInput(pygame.mouse.get_pos()):
                        print("Registrando...")
                        botonregistrar.click(self.screen)
                        usuario = caja.getText()
                        correo = caja2.getText()
                        contraseña = caja3.getText()
                        confirmcontra = caja4.getText()
                        #renderT = None
                        #print(contraseña)
                        lista = Item.valor(self)
                        response = validar.validarRegistro(usuario,correo,contraseña,confirmcontra,lista ,self.conexion, self.cursor)
                        if response == "OK":
                            return
                        else:
                            
                            textR = pygame.font.Font("graphics/font/joystix.ttf", 15)
                            renderT = textR.render(response, True, (255,0,0))
                            rect = renderT.get_rect(center=(SCREEN_WIDTH//2, 430))      
            pygame.display.update()

    def CargarKS(self):
        print("Cargando")
        self.progreso = 20
        
        self.clock = pygame.time.Clock()
        self.progreso = 30
        
        self.main_sound = pygame.mixer
        self.main_sound.music.load('audio/Monkberry Moon Delight.ogg')
        
        self.progreso = 50
        
        self.musica_personalizada = pygame.mixer.Sound("audio/bass-loops-006-with-drums-long-loop-120-bpm-6111.mp3")
        self.musica_instrumentos = pygame.mixer.Sound("audio/[CHIPTUNE] Pink Floyd - Have A Cigar.wav")

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
        print("inicializando niveles")
        self.downloaded_level.append(Level())
        print("primer nivel...")
        self.downloaded_level.append(Level_2(self.downloaded_level[0].player))
        print("segundo nivel...")
        
        self.level = self.downloaded_level[0]
        
        self.player = self.level.player
        
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
        DISPLAY_TIME_AFTER_TYPING = 2
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
                        self.Pausita = PausaMenu(self.main_sound,self.musica_personalizada,self.player,self.conexion,self.cursor ,self.screen)
                        xd = self.Pausita.show_menu(self.screen)
                        if xd == False:
                            self.main_sound.music.unpause()
                    if event.key == pygame.K_m:
                        self.main_sound.music.pause()
                        self.musica_personalizada.play(1)
                        listaIn = Item.valor(self)
                        self.Instrumentos = MInstrumentos(self.main_sound,self.musica_instrumentos, listaIn, self.player, self.conexion, self.cursor)#Cambiar la musica
                        regreso_de_minstrumentos = self.Instrumentos.mostrar_instrumentos()
                        if regreso_de_minstrumentos == False:
                            self.main_sound.music.unpause()
                    if event.key == pygame.K_n:
                        npc_name = NPC.obtener_npc()
                        
                        if npc_name == 'jimmy':
                            text = "Jimmy: Erm, tenemos buenas, malas y peores"
                            text2 = "Jimmy: ¿A que le temes?"
                            text3= "Jimmy: ¡VAAAAAA!"
                            text4= "Jimmy: Obvio noOooO"
                            text5= "Jimmy: Te voy a reprobar"
                            textos = [text,text2,text3,text4,text5]
                            eleccion = random.choice(textos)
                            show_text_box = True
                            text_finished_time = None
                            if show_text_box:
                                start_time = NPC.mostrar_caja_dialogo(self.screen, 200, 500, 950, 100, eleccion)
                                text_finished_time = start_time + len(eleccion) * 50
                                pygame.time.delay(1000)
                                show_text_box = False
                            if text_finished_time and pygame.time.get_ticks() > text_finished_time + DISPLAY_TIME_AFTER_TYPING * 1000:
                                text_finished_time = None
                        if npc_name == 'bernabe':
                            text = "Bernabe: Dame tu credencial, hijo"
                            text2 = "Bernabe: ¿No tienes clase hijo?"
                            textos = [text, text2]
                            eleccion = random.choice(textos)
                            show_text_box = True
                            text_finished_time = None
                            if show_text_box:
                                start_time = NPC.mostrar_caja_dialogo(self.screen, 200, 500, 950, 100, eleccion)
                                text_finished_time = start_time + len(eleccion) * 50
                                pygame.time.delay(1000)
                                show_text_box = False
                            if text_finished_time and pygame.time.get_ticks() > text_finished_time + DISPLAY_TIME_AFTER_TYPING * 1000:
                                text_finished_time = None
                        if npc_name == 'jesus':
                            text = "Jesus: ¿Has visto a mi robot?"
                            text2 = "Jesus: No sé, soy de progra"
                            textos = [text,text2]
                            eleccion = random.choice(textos)
                            show_text_box = True
                            text_finished_time = None
                            if show_text_box:
                                start_time = NPC.mostrar_caja_dialogo(self.screen, 200, 500, 950, 100, eleccion)
                                text_finished_time = start_time + len(eleccion) * 50
                                pygame.time.delay(1000)
                                show_text_box = False
                            if text_finished_time and pygame.time.get_ticks() > text_finished_time + DISPLAY_TIME_AFTER_TYPING * 1000:
                                text_finished_time = None
                        if npc_name == 'mixer':
                            pygame.mixer.music.pause()
                            self.mez = Mezcladora(self.player, self.conexion, self.cursor, self.screen)
                            regresar_mezcladora = self.mez.mostrar_menu_mezcladora()
                            if regresar_mezcladora == False:
                                pygame.mixer.music.unpause()
                    
                        
            self.screen.fill(self.color_level[self.currentLevelNum])
            self.level.run()
            
            #print(self.player.rect.topleft)
            
            
            if(eucDis(self.player.rect.topleft, (4001, 705))<70 and self.currentLevelNum != 1):
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
    
if __name__ == '__main__':
    print("inicializar juego")
    game = Game()
    threadLevel = threading.Thread(target=game.inicializar_level)
    threadLevel.start()
    game.logos()
    threadConectar = threading.Thread(target=game.conectarBase)
    threadConectar.start()
    sesion = game.Pantalla_incio()
    threadCargarKS = threading.Thread(target=game.CargarKS)
    threadCargarKS.start()
    game.mostrar_animacion_carga()
    threadLevel.join()
    game.run()