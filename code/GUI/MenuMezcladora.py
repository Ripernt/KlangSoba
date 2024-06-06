import pygame, settings, os, threading
from GUI.button import Button
from GUI.Entry import InputBox
from settings import *
from DB import validar
from tkinter import filedialog
from moviepy.editor import AudioFileClip, CompositeAudioClip
from pydub import AudioSegment

def mostrar_dialogo_guardar(mezclado, audio):
    global guardandoC, guardado
    direccion = filedialog.asksaveasfilename(initialdir="/", title="Guardar como", filetypes=(("wav files", "*.wav"), ("todos los archivos", "*.*")))
    print(direccion)
    _, extension = os.path.splitext(direccion)
    if(direccion != ""):
        if extension == ".wav":
            #mezclado.export(direccion, format="wav")
            
            mezclado.write_audiofile(direccion, fps=audio[0].fps)
        else:
            mezclado.write_audiofile(direccion+".wav", fps=audio[0].fps)
            #mezclado.export(direccion+".wav", format="wav")
        guardado = True
    guardandoC = False
#guardadoCorr = False
guardandoC = False
guardado = True



class Mezcladora():
    def __init__(self, player, conexion, cursor, screen): #= pygame.display.set_mode((settings.SCREEN_WIDTH,settings.SCREEN_HEIGHT))
        #self.lista_consumir = lista
        self.mezcladora = True
        self.screen = screen
        self.player = player
        self.conexion = conexion
        self.cursor = cursor
        self.lista_audios = []
        self.no_reproduciendo = True
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.can_mix = False
        self.can_mix2 = False
        self.permiso_de_mezcladora = False
        
        
              
    def mostrar_menu_mezcladora(self):
        
        pausado = False

        permiso_de_mezcladora = False

        self.fontsito = pygame.font.Font('graphics/font/joystix.ttf', 20)
        
        boton_regresar = Button(image=settings.botonRegresar, pos=(200,600),text_input="", font=self.fontsito,
                             base_color="#4D4D5C", hovering_color="#75E2EC")

        boton_mezclar = Button(image=settings.generalButton, pos=(SCREEN_WIDTH/2,500), text_input="Mezclar", font=self.fontsito,
                             base_color="#4D4D5C", hovering_color="#75E2EC")
        
        boton_guardar_mezcla = Button(image=settings.botonGuardarPista, pos=(1000,600),text_input="",font=self.fontsito,
                                base_color="#4D4D5C", hovering_color="#75E2EC")
        
        boton_reproducir_mezcla = Button(image=settings.botonGrabar, pos=(1050,600), text_input="", font=self.fontsito,
                                         base_color="#4D4D5C", hovering_color="#75E2EC")
        
        boton_pausar_mezcla = Button(image=settings.botonPausar, pos=(1100,600), text_input="", font=self.fontsito,
                                         base_color="#4D4D5C", hovering_color="#75E2EC")
        
        boton_borrar_mezcla = Button(image=settings.botonBorrarGrabacion, pos=(1150,600), text_input="", font=self.fontsito,
                                         base_color="#4D4D5C", hovering_color="#75E2EC")

        #Texto menu de instrumentos
        mezcladora_text = self.fontsito.render("Menu de mezcladora", True, "white") 
        mezcladora_rect = mezcladora_text.get_rect(center=(settings.SCREEN_WIDTH/2, settings.SCREEN_HEIGHT/11))

        fondo = pygame.image.load("graphics/elementos_graficos/fondosgenerico.png")
        fondo = pygame.transform.scale(fondo, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

        boton_archivo_musica1 = Button(image=settings.botonArchivoMusica, pos=(320,210), text_input="", font=self.fontsito,
                                       base_color="#4D4D5C", hovering_color="#75E2EC")

        boton_archivo_musica2 = Button(image=settings.botonArchivoMusica, pos=(320,310), text_input="", font=self.fontsito,
                                       base_color="#4D4D5C", hovering_color="#75E2EC")
        
        caja_archivo1 = InputBox((370,200,550,32), "", colorValue=[(0,0,0), (255,0,0)]) 
        caja_archivo2 = InputBox((370,300,550,32), "", colorValue=[(0,0,0), (255,0,0)]) 

        #Cosas para mezclar
        mezcladora_costo = 0
        paga_mezcladora = False
        pila_img = pygame.image.load("graphics/items/bateria.png")
        pila_img = pygame.transform.scale(pila_img,(50,50))
        pila_text = self.fontsito.render("x"+str(mezcladora_costo), True, "white")


        renderT = None

        while self.mezcladora:

            self.screen.fill((50,50,50))
            self.screen.blit(fondo,(0,0))

            self.screen.blit(mezcladora_text, mezcladora_rect)

            boton_archivo_musica1.cargar(self.screen)
            boton_archivo_musica2.cargar(self.screen)

            caja_archivo1.update(self.screen)
            caja_archivo2.update(self.screen)
            
            self.screen.blit(pila_img,(SCREEN_WIDTH/2,550))
            self.screen.blit(pila_text,(600,575))

            boton_regresar.cargar(self.screen)

            boton_guardar_mezcla.cargar(self.screen)

            if self.no_reproduciendo:
                boton_reproducir_mezcla.cargar(self.screen)

            if not self.no_reproduciendo:
                boton_pausar_mezcla.cargar(self.screen)

            boton_mezclar.cargar(self.screen)
            boton_mezclar.cambiar_color(pygame.mouse.get_cursor())

            boton_borrar_mezcla.cargar(self.screen)

            if renderT is not None:
                self.screen.blit(renderT, rect)

            events = pygame.event.get()

            for event in events:

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if boton_regresar.checkForInput(pygame.mouse.get_pos()):
                        boton_regresar.click(self.screen)
                        self.mezcladora = False
                        if not self.no_reproduciendo:
                            self.pista_audio_mezclada.stop()
                        return self.mezcladora
                    #Accion para agarrar un archivo .wav
                    if boton_archivo_musica1.checkForInput(pygame.mouse.get_pos()):
                        boton_archivo_musica1.click(self.screen)
                        archivo_wav = filedialog.askopenfilename(title="Selecciona un archivo .wav")
                        caja_archivo1.setText(str(archivo_wav))
                        self.lista_audios.append(str(archivo_wav))
                        self.can_mix = True
                        
                    #Accion para agarrar un archivo .wav    
                    if boton_archivo_musica2.checkForInput(pygame.mouse.get_pos()):
                        boton_archivo_musica2.click(self.screen)
                        archivo_wav2 = filedialog.askopenfilename(title="Selecciona un archivo .wav")
                        caja_archivo2.setText(str(archivo_wav2))
                        self.lista_audios.append(str(archivo_wav2))
                        self.can_mix2 = True
                        
                    #Accion para mezclar pistas de audio                  
                    if boton_mezclar.checkForInput(pygame.mouse.get_pos()):
                        boton_mezclar.click(self.screen) 
                        if mezcladora_costo <= self.player.items_num[0] and self.lista_audios != [] and self.can_mix == True and self.can_mix2 == True and self.permiso_de_mezcladora == False:
                            constante = self.player.items_num[0] - mezcladora_costo
                            self.player.items_num[0] = constante

                            validar.insertar_items(self.player.items_num, self.conexion, self.cursor)
                            paga_mezcladora = True
                            if paga_mezcladora == True:
                                audio_clips = [AudioFileClip(file) for file in self.lista_audios]
                                result_audio = CompositeAudioClip(audio_clips)
                                result_audio.write_audiofile("resultado.wav", fps=audio_clips[0].fps)
                                pygame.time.wait(2)
                                self.lista_audios.clear()
                                caja_archivo1.setText("")
                                caja_archivo2.setText("")
                                self.pista_audio_mezclada =  pygame.mixer.Sound("resultado.wav")
                                self.permiso_de_mezcladora = True
                                mezcla_text = "Se ha mezclado!"
                                textR = pygame.font.Font("graphics/font/joystix.ttf", 15)
                                renderT = textR.render(mezcla_text, True, (255,0,0))
                                rect = renderT.get_rect(center=(SCREEN_WIDTH//2, 150))

                        else:
                            error_mezclar = "Debes de poner 2 pistas de audio para poder mezclar"
                            textR = pygame.font.Font("graphics/font/joystix.ttf", 15)
                            renderT = textR.render(error_mezclar, True, (255,0,0))
                            rect = renderT.get_rect(center=(SCREEN_WIDTH//2, 150))
                            
                    if boton_guardar_mezcla.checkForInput(pygame.mouse.get_pos()):
                        boton_guardar_mezcla.click(self.screen)
                        if paga_mezcladora == True and self.permiso_de_mezcladora == True:
                            thread = threading.Thread(target=mostrar_dialogo_guardar, args=(result_audio,audio_clips,))
                            thread.start()
                            guardar_text_mezcla = "Guardando la mezcla" 
                            textR = pygame.font.Font("graphics/font/joystix.ttf", 15)
                            renderT = textR.render(guardar_text_mezcla, True, (255,0,0))
                            rect = renderT.get_rect(center=(SCREEN_WIDTH//2, 150))
                        else:
                            boton_guardar_mezcla.click(self.screen)
                            #print("Debes de mezclar algo primero para poder guardar una mezcla")
                            no_guardar_mezcla_text = "Debes de mezclar algo primero para poder guardar una mezcla"
                            textR = pygame.font.Font("graphics/font/joystix.ttf", 15)
                            renderT = textR.render(no_guardar_mezcla_text, True, (255,0,0))
                            rect = renderT.get_rect(center=(SCREEN_WIDTH//2, 150))

                    if boton_reproducir_mezcla.checkForInput(pygame.mouse.get_pos()):
                        boton_reproducir_mezcla.click(self.screen)
                    
                        if self.no_reproduciendo == True and self.permiso_de_mezcladora == True:
                            self.no_reproduciendo = False
                            if pausado == False:
                                pista = self.pista_audio_mezclada.play()
                                
                            else:
                                pista.unpause()
                        else:
                            boton_reproducir_mezcla.click(self.screen)
                            print("Debes de tener algo mezclado para poder reproducir algo")
                            reproducir_text = "Debes de tener algo mezclado para poder reproducir algo"
                            textR = pygame.font.Font("graphics/font/joystix.ttf", 15)
                            renderT = textR.render(reproducir_text, True, (255,0,0))
                            rect = renderT.get_rect(center=(SCREEN_WIDTH//2, 150))
                            
                    if boton_pausar_mezcla.checkForInput(pygame.mouse.get_pos()) and self.no_reproduciendo == False and self.permiso_de_mezcladora == True:
                        boton_pausar_mezcla.click(self.screen)
                        self.no_reproduciendo = True
                        pausado = True
                        pista.pause()
                    
                    else:
                        print("nomas")

                    if boton_borrar_mezcla.checkForInput(pygame.mouse.get_pos()):
                        boton_borrar_mezcla.click(self.screen)
                        
                        if self.no_reproduciendo == True and self.permiso_de_mezcladora == True:
                            
                            self.permiso_de_mezcladora = False
                            pausado = False
                            self.can_mix2 = False
                            self.can_mix = False
                            borrar_mezcla_text = " Se ha borrado la mezcla"
                            textR = pygame.font.Font("graphics/font/joystix.ttf", 15)
                            renderT = textR.render(borrar_mezcla_text, True, (255,0,0))
                            rect = renderT.get_rect(center=(SCREEN_WIDTH//2, 150))                        
                        else:
                            boton_borrar_mezcla.click(self.screen)
                            print("Necesitas parar el audio para poder borrarlo o grabar una mezcla")
                            error_borrar_mezcla_text = "Necesitas parar el audio para poder borrarlo o grabar una mezcla"
                            textR = pygame.font.Font("graphics/font/joystix.ttf", 15)
                            renderT = textR.render(error_borrar_mezcla_text, True, (255,0,0))
                            rect = renderT.get_rect(center=(SCREEN_WIDTH//2, 150))
                        
                    
                        
            pygame.display.update()
