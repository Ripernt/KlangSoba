import pygame, settings, time, wave, threading
import numpy as np

from tkinter import filedialog as fd
import os
from pydub import AudioSegment

from GUI.button2 import Button2
from GUI.button import Button
from pygame.locals import *

position = 0



#Exportar archivo
def mostrar_dialogo_guardar(grabacion):
    global guardandoC, guardado
    direccion = fd.asksaveasfilename(initialdir="/", title="Guardar como", filetypes=(("wav files", "*.wav"), ("todos los archivos", "*.*")))
    print(direccion)
    _, extension = os.path.splitext(direccion)
    if(direccion != ""):
        if extension == ".wav":
            grabacion.export(direccion, format="wav")
        else:
            grabacion.export(direccion+".wav", format="wav")
        guardado = True
    guardandoC = False
# guardadoCorr = False
guardandoC = False
guardado = True

class InterfazPiano:

    def __init__(self, screen, instrumentos):
        self.instrumentos = instrumentos
        self.screen = screen
        self.piano = True
        self.fontsito = pygame.font.Font('graphics/font/joystix.ttf', 20)
        
        #Variables para la grabación del piano
        self.grabar = False
        self.Dgrabar = 0
        self.Egrabar = 0

        self.Duracion = 0
        self.emptyTime = 0

        self.tiempos = []
        self.teclas = []

        self.tiempo = "0:0"

        #Teclas para tocar el piano
        #2,4,5,8,9,0,'
        #qwertuiop
        #asfgjkl
        #zxcvbnm,.

    def background(self):

            global position
            fondo = pygame.image.load("graphics/elementos_graficos/pianoBG.png")
            fondo = pygame.transform.scale(fondo, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
            self.screen.fill((0,0,0))

            self.screen.blit(fondo,(position,0))
            self.screen.blit(fondo,(fondo.get_width()+position,0))

            position -= 5

            if abs(position) > fondo.get_width():
                position = 0

    def mostrar_menu_piano(self):
        global guardandoC, guardado
        self.screen.fill((50, 50, 50))
        
        boton=pygame.image.load("graphics/elementos_graficos/botonT.png")
        boton=pygame.transform.scale(boton,(50,50))

        # c
        self.botonTt = Button2(image=settings.botonDOPiano, pos=(35,620), text_input="t", font=self.fontsito,base_color="#4D4D5C", hovering_color="75E2EC")
        # c#
        self.botonT5 = Button2(image=settings.botonNEGRAPiano, pos=(65,565), text_input="5", font=self.fontsito,base_color="#4D4D5C", hovering_color="75E2EC")
        # d
        self.botonTr = Button2(image=settings.botonREPiano, pos=(96,620), text_input="r", font=self.fontsito,base_color="#4D4D5C", hovering_color="75E2EC")
        # d#
        self.botonT4 = Button2(image=settings.botonNEGRAPiano, pos=(126,565), text_input="4", font=self.fontsito,base_color="#4D4D5C", hovering_color="75E2EC")
        # e
        self.botonTe = Button2(image=settings.botonMIPiano, pos=(157,620), text_input="e", font=self.fontsito,base_color="#4D4D5C", hovering_color="75E2EC")
        # f
        self.botonTw = Button2(image=settings.botonDOPiano, pos=(218,620), text_input="w", font=self.fontsito,base_color="#4D4D5C", hovering_color="75E2EC")
        # f#
        self.botonT2 = Button2(image=settings.botonNEGRAPiano, pos=(248,565), text_input="2", font=self.fontsito,base_color="#4D4D5C", hovering_color="75E2EC")
        # g
        self.botonTa = Button2(image=settings.botonREPiano, pos=(279,620), text_input="a", font=self.fontsito,base_color="#4D4D5C", hovering_color="75E2EC")
        # g#
        self.botonTq = Button2(image=settings.botonNEGRAPiano, pos=(309,565), text_input="q", font=self.fontsito,base_color="#4D4D5C", hovering_color="75E2EC")
        # a
        self.botonTz = Button2(image=settings.botonREPiano, pos=(340,620), text_input="z", font=self.fontsito,base_color="#4D4D5C", hovering_color="75E2EC")
        # a#
        self.botonTs = Button2(image=settings.botonNEGRAPiano, pos=(370,565), text_input="s", font=self.fontsito,base_color="#4D4D5C", hovering_color="75E2EC")
        # b
        self.botonTx = Button2(image=settings.botonMIPiano, pos=(401,620), text_input="x", font=self.fontsito,base_color="#4D4D5C", hovering_color="75E2EC")
        # c1
        self.botonTc = Button2(image=settings.botonDOPiano, pos=(462,620), text_input="c", font=self.fontsito,base_color="#4D4D5C", hovering_color="75E2EC")
        # c1#
        self.botonTf = Button2(image=settings.botonNEGRAPiano, pos=(492,565), text_input="f", font=self.fontsito,base_color="#4D4D5C", hovering_color="75E2EC")
        # d1
        self.botonTv = Button2(image=settings.botonREPiano, pos=(523,620), text_input="v", font=self.fontsito,base_color="#4D4D5C", hovering_color="75E2EC")
        # d1#
        self.botonTg = Button2(image=settings.botonNEGRAPiano, pos=(553,565), text_input="g", font=self.fontsito,base_color="#4D4D5C", hovering_color="75E2EC")
        # e1
        self.botonTb = Button2(image=settings.botonMIPiano, pos=(584,620), text_input="b", font=self.fontsito,base_color="#4D4D5C", hovering_color="75E2EC")
        # f1
        self.botonTn = Button2(image=settings.botonDOPiano, pos=(645,620), text_input="n", font=self.fontsito,base_color="#4D4D5C", hovering_color="75E2EC")
        # f1#
        self.botonTj = Button2(image=settings.botonNEGRAPiano, pos=(675,565), text_input="j", font=self.fontsito,base_color="#4D4D5C", hovering_color="75E2EC")
        # g1
        self.botonTm = Button2(image=settings.botonREPiano, pos=(706,620), text_input="m", font=self.fontsito,base_color="#4D4D5C", hovering_color="75E2EC")
        # g1#
        self.botonTk = Button2(image=settings.botonNEGRAPiano, pos=(736,565), text_input="k", font=self.fontsito,base_color="#4D4D5C", hovering_color="75E2EC")
        # a1
        self.botonTComa = Button2(image=settings.botonREPiano, pos=(767,620), text_input=",", font=self.fontsito,base_color="#4D4D5C", hovering_color="75E2EC")
        # a1#
        self.botonTl = Button2(image=settings.botonNEGRAPiano, pos=(797,565), text_input="l", font=self.fontsito,base_color="#4D4D5C", hovering_color="75E2EC")
        # b1
        self.botonTPunto = Button2(image=settings.botonMIPiano, pos=(828,620), text_input=".", font=self.fontsito,base_color="#4D4D5C", hovering_color="75E2EC")
        # c2
        self.botonTFlechaArriba = Button2(image=settings.botonDOPiano, pos=(889,620),text_input="↑", font=self.fontsito, base_color="#4D4D5C", hovering_color="75E2EC")
        # c2#
        self.botonTFlechaAbajo = Button2(image=settings.botonNEGRAPiano, pos=(919,565),text_input="↓" , font=self.fontsito, base_color="#4D4D5C", hovering_color="75E2EC")
        # d2
        self.botonTComilla = Button2(image=settings.botonREPiano, pos=(950,620), text_input="'", font=self.fontsito,base_color="#4D4D5C", hovering_color="75E2EC")
        # d2#
        self.botonTF10 = Button2(image=settings.botonNEGRAPiano, pos=(980,565), text_input="F10", font=self.fontsito,base_color="#4D4D5C", hovering_color="75E2EC")
        # e2
        self.botonTBorrar = Button2(image=settings.botonMIPiano, pos=(1011,620), text_input="DEL", font=self.fontsito,base_color="#4D4D5C", hovering_color="75E2EC")
        # f2
        self.botonTp = Button2(image=settings.botonDOPiano, pos=(1072,620), text_input="p", font=self.fontsito,base_color="#4D4D5C", hovering_color="75E2EC")
        # f2#
        self.botonT0 = Button2(image=settings.botonNEGRAPiano, pos=(1102,565), text_input="0", font=self.fontsito,base_color="#4D4D5C", hovering_color="75E2EC")
        # g2
        self.botonTo = Button2(image=settings.botonREPiano, pos=(1133,620), text_input="o", font=self.fontsito,base_color="#4D4D5C", hovering_color="75E2EC")
        # g2#
        self.botonT9 = Button2(image=settings.botonNEGRAPiano, pos=(1163,565), text_input="9", font=self.fontsito,base_color="#4D4D5C", hovering_color="75E2EC")
        # a2
        self.botonTi = Button2(image=settings.botonREPiano, pos=(1194,620), text_input="i", font=self.fontsito,base_color="#4D4D5C", hovering_color="75E2EC")
        # a2#
        self.botonT8 = Button2(image=settings.botonNEGRAPiano, pos=(1224,565), text_input="8", font=self.fontsito,base_color="#4D4D5C", hovering_color="75E2EC")
        # b2
        self.botonTu = Button2(image=settings.botonMIPiano, pos=(1255,620), text_input="u", font=self.fontsito,base_color="#4D4D5C", hovering_color="75E2EC")

        #self.pianito = pygame.image.load('graphics/elementos_graficos/pianoPianito.png')
        #self.pianito = pygame.transform.scale(self.pianito, (900,300))
        sep = self.screen.get_width()//20*2

        #Boton guardar pista
        self.botonGuard = Button(image=settings.botonGuardarPista, pos=(1200,450), text_input="", font=self.fontsito,base_color="#4D4D5C", hovering_color="75E2EC")    
        self.botonGuard.enable = False

        #Boton grabar
        self.botonG = Button(image=settings.botonGrabar, pos=(100,450), text_input="", font=self.fontsito,base_color="#4D4D5C", hovering_color="75E2EC")
        #Boton dejar de grabar
        self.botonSG = Button(image=settings.botonStopGrabar, pos=(180,450), text_input="", font=self.fontsito,base_color="#4D4D5C", hovering_color="75E2EC")
        #Boton no grabando
        self.Nograbando = Button(image=settings.botonNoGrabando, pos=(260,450),text_input="",font=self.fontsito,base_color="#4D4D5C", hovering_color="75E2EC")

        #Boton grabando
        self.Grabando = Button(image=settings.botonGrabando, pos=(260,450),text_input="",font=self.fontsito,base_color="#4D4D5C", hovering_color="75E2EC")
        
        #Boton Borrar
        self.botonDel = Button(image=settings.botonGuardarPista, pos=(1100,450), text_input="Borrar", font=self.fontsito,base_color="#4D4D5C", hovering_color="75E2EC")
        self.botonDel.enable = False

        self.salir_botton = Button(image=boton, pos=(100,100), text_input="",font=self.fontsito,base_color="#4D4D5C",hovering_color="#75E2EC")

        #Teclas para tocar el piano
        self.pianoKey = ['c',  'c#',  'd',  'd#',  'e',  'f',  'f#',  'g',  'g#',  'a',  'a#',  'b',
                'c1', 'c1#', 'd1', 'd1#', 'e1', 'f1', 'f1#', 'g1', 'g1#', 'a1', 'a1#', 'b1',
                'c2', 'c2#', 'd2', 'd2#', 'e2', 'f2', 'f2#', 'g2', 'g2#', 'a2', 'a2#', 'b2']
        self.boardKey = [pygame.K_t, pygame.K_5, pygame.K_r, pygame.K_4, pygame.K_e, pygame.K_w,
                pygame.K_2, pygame.K_a, pygame.K_q, pygame.K_z, pygame.K_s, pygame.K_x,
                pygame.K_c, pygame.K_f, pygame.K_v, pygame.K_g, pygame.K_b, pygame.K_n,
                pygame.K_j, pygame.K_m, pygame.K_k, pygame.K_COMMA, pygame.K_l, pygame.K_PERIOD,
                pygame.K_UP, pygame.K_DOWN, pygame.K_QUOTE, pygame.K_F10,
                pygame.K_BACKSPACE, pygame.K_p, pygame.K_0, pygame.K_o, pygame.K_9,
                pygame.K_i, pygame.K_8, pygame.K_u]
        self.keyDict = {bk: pk for bk, pk in zip(self.boardKey, self.pianoKey)}
        self.colorDict = {bk: (4*i, 4*i, 4*i) for i, bk in enumerate(self.boardKey, 1)}
        pygame.mixer.set_num_channels(256)



        while self.piano:

            self.background()

            if self.grabar:
                print(self.teclas)

            #self.screen.fill((50,50,50))            
            
            self.salir_botton.cargar(self.screen)
            self.salir_botton.cambiar_color(pygame.mouse.get_pos())

            if not self.grabar:
                self.botonG.cargar(self.screen)
                #Carga de luz de grabando apagada
                self.Nograbando.cargar(self.screen)
            
            if self.grabar:
                self.botonSG.cargar(self.screen)
                #imagen de luz de grabando encendida
                self.Grabando.cargar(self.screen)


            #self.botonG.cargar(self.screen)
            
            #self.botonSG.cargar(self.screen)
        
            self.botonT2.cargar(self.screen)
            #self.botonT2.cambiar_color(pygame.mouse.get_pos())

            self.botonT4.cargar(self.screen) 
            #self.botonT4.cambiar_color(pygame.mouse.get_pos())

            self.botonT5.cargar(self.screen) 
            #self.botonT8.cambiar_color(pygame.mouse.get_pos())

            self.botonT8.cargar(self.screen)

            self.botonT9.cargar(self.screen)  
            #self.botonT9.cambiar_color(pygame.mouse.get_pos())

            self.botonT0.cargar(self.screen) 
            #self.botonT0.cambiar_color(pygame.mouse.get_pos())

            self.botonTComilla.cargar(self.screen)  
            #self.botonTComilla.cambiar_color(pygame.mouse.get_pos())

            self.botonTq.cargar(self.screen)  
            #self.botonTq.cambiar_color(pygame.mouse.get_pos())

            self.botonTw.cargar(self.screen) 
            #self.botonTw.cambiar_color(pygame.mouse.get_pos()) 

            self.botonTe.cargar(self.screen) 
            #self.botonTe.cambiar_color(pygame.mouse.get_pos()) 

            self.botonTr.cargar(self.screen)  
            #self.botonTr.cambiar_color(pygame.mouse.get_pos())

            self.botonTt.cargar(self.screen)  
            #self.botonTt.cambiar_color(pygame.mouse.get_pos())

            self.botonTu.cargar(self.screen)  
            #self.botonTu.cambiar_color(pygame.mouse.get_pos())

            self.botonTi.cargar(self.screen)  
            #self.botonTi.cambiar_color(pygame.mouse.get_pos())

            self.botonTo.cargar(self.screen)  
            #self.botonTo.cambiar_color(pygame.mouse.get_pos())

            self.botonTp.cargar(self.screen)  
            #self.botonTp.cambiar_color(pygame.mouse.get_pos())

            self.botonTa.cargar(self.screen) 
            #self.botonTa.cambiar_color(pygame.mouse.get_pos())

            self.botonTs.cargar(self.screen)  
            #self.botonTs.cambiar_color(pygame.mouse.get_pos())

            self.botonTf.cargar(self.screen)  
            #self.botonTf.cambiar_color(pygame.mouse.get_pos())

            self.botonTg.cargar(self.screen) 
            #self.botonTg.cambiar_color(pygame.mouse.get_pos())

            self.botonTj.cargar(self.screen)  
            #self.botonTj.cambiar_color(pygame.mouse.get_pos())

            self.botonTk.cargar(self.screen)  
            #self.botonTk.cambiar_color(pygame.mouse.get_pos())

            self.botonTl.cargar(self.screen)  
            #self.botonTl.cambiar_color(pygame.mouse.get_pos())

            self.botonTz.cargar(self.screen)  
            #self.botonTz.cambiar_color(pygame.mouse.get_pos())

            self.botonTx.cargar(self.screen)  
            #self.botonTx.cambiar_color(pygame.mouse.get_pos())

            self.botonTc.cargar(self.screen)  
            #self.botonTc.cambiar_color(pygame.mouse.get_pos())

            self.botonTv.cargar(self.screen)  
            #self.botonTv.cambiar_color(pygame.mouse.get_pos())

            self.botonTb.cargar(self.screen)  
            #self.botonTb.cambiar_color(pygame.mouse.get_pos())

            self.botonTn.cargar(self.screen)  
            #self.botonTn.cambiar_color(pygame.mouse.get_pos())

            self.botonTm.cargar(self.screen)  
            #self.botonTm.cambiar_color(pygame.mouse.get_pos())

            self.botonTComa.cargar(self.screen)  
            #self.botonTComa.cambiar_color(pygame.mouse.get_pos())

            self.botonTPunto.cargar(self.screen)  
            #self.botonTPunto.cambiar_color(pygame.mouse.get_pos())

            self.botonTFlechaArriba.cargar(self.screen)

            self.botonTFlechaAbajo.cargar(self.screen)

            self.botonTF10.cargar(self.screen)

            self.botonTBorrar.cargar(self.screen)           
            #self.screen.blit(self.pianito, (200,370))


            
            #Carga el boton GuardarPista
            self.botonGuard.cargar(self.screen)
            self.botonGuard.enable = not guardado

            self.botonDel.cargar(self.screen)
            self.botonDel.enable = not guardado

            self.botonTBorrar.cargar(self.screen)

            events = pygame.event.get()

            if(not guardado or self.grabar):
                if(self.grabar):
                    self.tiempo = str((pygame.time.get_ticks()-self.Egrabar-self.emptyTime)/1000).split('.')
                
                segundos = self.tiempo[0]
                milisegundos = self.tiempo[1]+"0"*(3-len(self.tiempo[1]))
                r = self.fontsito.render(segundos+":"+milisegundos,True,"#ffffff")
            else:
                r = self.fontsito.render("0:0",True,"#ffffff")
            rect = r.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//10*6))
            self.screen.blit(r,rect)


            for event in events:    
                #Salir
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.salir_botton.checkForInput(pygame.mouse.get_pos()):
                        self.piano = False
                        self.instrumentos = True
                        #self.instrumentos = True
                        self.salir_botton.click(self.screen)
                        #self.musica_almanaque.stop() //Agregar
                        return self.piano

                    if self.botonSG.checkForInput(pygame.mouse.get_pos()) and self.grabar:
                        self.botonSG.click(self.screen)
                        self.grabar = False
                        self.Dgrabar = pygame.time.get_ticks()
                        guardado = False
                    
                    elif self.botonG.checkForInput(pygame.mouse.get_pos()) and not self.grabar and not guardandoC:
                        self.botonG.click(self.screen)
                        self.grabar = True

                        if not guardado:
                            self.emptyTime += pygame.time.get_ticks()-self.Dgrabar
                        else:
                            self.Egrabar = pygame.time.get_ticks()
                            self.emptyTime = 0
                            self.Duracion = 0
                            self.teclas = []
                            self.tiempos = []
                    
                    elif self.botonDel.checkForInput(pygame.mouse.get_pos()) and not self.grabar and not guardandoC and not guardado:  
                        self.botonDel.click(self.screen)
                        self.grabar = False
                        guardado = True
                        self.emptyTime = 0
                        self.Duracion = 0
                        self.teclas = []
                        self.tiempos = []

                    elif self.botonGuard.checkForInput(pygame.mouse.get_pos()) and not self.grabar and not guardado and not guardandoC:
                        guardadoC = True
                        self.botonGuard.click(self.screen)
                        self.Duracion = self.Dgrabar-self.Egrabar-self.emptyTime
                        #Crear audio vacio
                        grabacion = AudioSegment.silent(duration=self.Duracion,frame_rate=44100)
                        
                        for i, t in enumerate(self.teclas):
                            fileName = "audio/audios/" + str(self.keyDict[t]) + ".wav"
                            teclaAudio = AudioSegment.from_file(fileName,format="wav")
                            grabacion = grabacion.overlay(teclaAudio, position=self.tiempos[i])
                        # Iniciar el hilo de tkinter
                        thread = threading.Thread(target=mostrar_dialogo_guardar, args=(grabacion,))
                        thread.start()

                if event.type == pygame.KEYUP:
                    if event.key == K_2:
                        self.botonT2Neg.unclick(self.screen)                        
                    if event.key == K_4:
                        self.botonT4Neg.unclick(self.screen)
                    if event.key == K_5:
                        self.botonT5Neg.unclick(self.screen)
                    if event.key == K_8:
                        self.botonT8Neg.unclick(self.screen)
                    if event.key == K_9:
                        self.botonT9Neg.unclick(self.screen)
                    if event.key == K_0:
                        self.botonT0Neg.unclick(self.screen)
                    if event.key == K_QUOTE:
                        self.botonTComilla.unclick(self.screen)                
                    if event.key == K_q:
                        self.botonTqNeg.unclick(self.screen)
                    if event.key == K_w:
                        self.botonTw.unclick(self.screen)
                    if event.key == K_e:
                        self.botonTe.unclick(self.screen)
                    if event.key == K_r:
                        self.botonTr.unclick(self.screen)
                    if event.key == K_t:
                        self.botonTt.unclick(self.screen)
                    if event.key == K_u:
                        self.botonTu.unclick(self.screen)
                    if event.key == K_i:
                        self.botonTi.unclick(self.screen)
                    if event.key == K_o:
                        self.botonTo.unclick(self.screen)
                    if event.key == K_p:
                        self.botonTp.unclick(self.screen)
                    if event.key == K_a:
                        self.botonTa.unclick(self.screen)
                    if event.key == K_s:
                        self.botonTsNeg.unclick(self.screen)
                    if event.key == K_f:
                        self.botonTfNeg.unclick(self.screen)  
                    if event.key == K_g:
                        self.botonTgNeg.unclick(self.screen)
                    if event.key == K_j:
                        self.botonTjNeg.unclick(self.screen)
                    if event.key == K_k:
                        self.botonTkNeg.unclick(self.screen)
                    if event.key == K_l:
                        self.botonTlNeg.unclick(self.screen)
                    if event.key == K_z:
                        self.botonTz.unclick(self.screen)
                    if event.key == K_x:
                        self.botonTx.unclick(self.screen)
                    if event.key == K_c:
                        self.botonTc.unclick(self.screen)
                    if event.key == K_v:
                        self.botonTv.unclick(self.screen)
                    if event.key == K_b:
                        self.botonTb.unclick(self.screen)
                    if event.key == K_n:
                        self.botonTn.unclick(self.screen)
                    if event.key == K_m:
                        self.botonTm.unclick(self.screen)
                    if event.key == K_COMMA:
                        self.botonTComa.unclick(self.screen)
                    if event.key == K_PERIOD:
                        self.botonTPunto.unclick(self.screen)
                    if event.key == K_F10:
                        self.botonTFNeg10.unclick(self.screen)
                    if event.key == K_UP:
                        self.botonTFNeglechaArriba.unclick(self.screen)
                    if event.key == K_DOWN:
                        self.botonTFNeglechaAbajo.unclick(self.screen)
                    if event.key == K_BACKSPACE:
                        self.botonTBorrar.unclick(self.screen)

                if event.type == pygame.KEYDOWN:
                    if event.key in self.keyDict.keys():
                        fileName = "audio/audios/" + str(self.keyDict[event.key]) + ".wav"
                        pygame.mixer.Sound(fileName).play()
                        if self.grabar:
                            self.teclas.append(event.key)
                            self.tiempos.append(pygame.time.get_ticks()-self.Egrabar-self.emptyTime)
                        
                    if event.key == K_2:
                        self.botonT2.click(self.screen)                        
                    if event.key == K_4:
                        self.botonT4.click(self.screen)
                    if event.key == K_5:
                        self.botonT5.click(self.screen)
                    if event.key == K_8:
                        self.botonT8.click(self.screen)
                    if event.key == K_9:
                        self.botonT9.click(self.screen)
                    if event.key == K_0:
                        self.botonT0.click(self.screen)
                    if event.key == K_QUOTE:
                        self.botonTComilla.click(self.screen)                
                    if event.key == K_q:
                        self.botonTq.click(self.screen)
                    if event.key == K_w:
                        self.botonTw.click(self.screen)
                    if event.key == K_e:
                        self.botonTe.click(self.screen)
                    if event.key == K_r:
                        self.botonTr.click(self.screen)
                    if event.key == K_t:
                        self.botonTt.click(self.screen)
                    if event.key == K_u:
                        self.botonTu.click(self.screen)
                    if event.key == K_i:
                        self.botonTi.click(self.screen)
                    if event.key == K_o:
                        self.botonTo.click(self.screen)
                    if event.key == K_p:
                        self.botonTp.click(self.screen)
                    if event.key == K_a:
                        self.botonTa.click(self.screen)
                    if event.key == K_s:
                        self.botonTs.click(self.screen)
                    if event.key == K_f:
                        self.botonTf.click(self.screen)  
                    if event.key == K_g:
                        self.botonTg.click(self.screen)
                    if event.key == K_j:
                        self.botonTj.click(self.screen)
                    if event.key == K_k:
                        self.botonTk.click(self.screen)
                    if event.key == K_l:
                        self.botonTl.click(self.screen)
                    if event.key == K_z:
                        self.botonTz.click(self.screen)
                    if event.key == K_x:
                        self.botonTx.click(self.screen)
                    if event.key == K_c:
                        self.botonTc.click(self.screen)
                    if event.key == K_v:
                        self.botonTv.click(self.screen)
                    if event.key == K_b:
                        self.botonTb.click(self.screen)
                    if event.key == K_n:
                        self.botonTn.click(self.screen)
                    if event.key == K_m:
                        self.botonTm.click(self.screen)
                    if event.key == K_COMMA:
                        self.botonTComa.click(self.screen)
                    if event.key == K_PERIOD:
                        self.botonTPunto.click(self.screen)
                    if event.key == K_F10:
                        self.botonTF10.click(self.screen)
                    if event.key == K_UP:
                        self.botonTFlechaArriba.click(self.screen)
                    if event.key == K_DOWN:
                        self.botonTFlechaAbajo.click(self.screen)
                    if event.key == K_BACKSPACE:
                        self.botonTBorrar.click(self.screen)
                
                        
                                              
                pygame.display.update()