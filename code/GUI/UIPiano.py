import pygame, sys, pyaudio, settings
from GUI.button import Button

class InterfazPiano:

    def __init__(self, screen):
        self.screen = screen
        self.piano = True
        self.fontsito = pygame.font.Font('graphics/font/joystix.ttf', 20)


    def mostrar_menu_piano(self):
        self.screen.fill((50,50,50))
        fondo = pygame.image.load("graphics/elementos_graficos/Menuinstrumentos.png")
        fondo = pygame.transform.scale(fondo, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        boton=pygame.image.load("graphics/elementos_graficos/botonT.png")
        boton=pygame.transform.scale(boton,(50,50))

        self.pianito = pygame.image.load('graphics/elementos_graficos/pianoPianito.png')
        self.pianito = pygame.transform.scale(self.pianito, (900,300))

        self.salir_botton = Button(image=boton, pos=(100,100), text_input="",font=self.fontsito,base_color="#4D4D5C",hovering_color="#75E2EC")

        #Teclas para tocar el piano
        self.pianoKey = ['c',  'c#',  'd',  'd#',  'e',  'f',  'f#',  'g',  'g#',  'a',  'a#',  'b',
                'c1', 'c1#', 'd1', 'd1#', 'e1', 'f1', 'f1#', 'g1', 'g1#', 'a1', 'a1#', 'b1',
                'c2', 'c2#', 'd2', 'd2#', 'e2', 'f2', 'f2#', 'g2', 'g2#', 'a2', 'a2#', 'b2']
        self.boardKey = [pygame.K_t, pygame.K_5, pygame.K_r, pygame.K_4, pygame.K_e, pygame.K_w,
                pygame.K_2, pygame.K_a, pygame.K_q, pygame.K_z, pygame.K_s, pygame.K_x,
                pygame.K_c, pygame.K_f, pygame.K_v, pygame.K_g, pygame.K_b, pygame.K_n,
                pygame.K_j, pygame.K_m, pygame.K_k, pygame.K_COMMA, pygame.K_l, pygame.K_PERIOD,
                pygame.K_SLASH, pygame.K_SEMICOLON, pygame.K_QUOTE, pygame.K_RIGHTBRACKET,
                pygame.K_LEFTBRACKET, pygame.K_p, pygame.K_0, pygame.K_o, pygame.K_9,
                pygame.K_i, pygame.K_8, pygame.K_u]
        self.keyDict = {bk: pk for bk, pk in zip(self.boardKey, self.pianoKey)}
        self.colorDict = {bk: (4*i, 4*i, 4*i) for i, bk in enumerate(self.boardKey, 1)}
        pygame.mixer.set_num_channels(256)


        while self.piano:

            self.salir_botton.cargar(self.screen)
            self.salir_botton.cambiar_color(pygame.mouse.get_pos())
            
            self.screen.blit(self.pianito, (200,370))

            events = pygame.event.get()

            for event in events:
                #Salir
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.salir_botton.checkForInput(pygame.mouse.get_pos()):
                        self.piano = False
                        self.salir_botton.click(self.screen)
                        #self.musica_almanaque.stop() //Agregar
                        return self.piano
                if event.type == pygame.KEYDOWN:
                    if event.key in self.keyDict.keys():
                        #print(self.keyDict.keys())
                        fileName = "audio/audios/" + str(self.keyDict[event.key]) + ".wav"
                        pygame.mixer.Sound(fileName).play()
                pygame.display.update()
        
