import pygame
import sys
from GUI.button import Button
from tkinter import messagebox
import settings
from logros import Logros
clock = pygame.time.Clock() 



def Movimiento_suave(bar_x=0,bar_y=0,square_x=None,square_y=None, error=0.75):
    #se lleva acabo el movimineto suave

    errorX = bar_x - square_x
    errorY = bar_y - square_y

    #se lleva acabo la correccio proporcional
    correccionX = errorX*error
    correccionY = errorY*error

    #se aplica las nuevas proporciones
    nuevoX = bar_x - correccionX
    nuevoY = bar_y - correccionY

    return (nuevoX,nuevoY)

class BarraDeVida:
    
    def __init__(self, screen):
        from level import YSortCameraGroup   
        # Inicializar Pygame
        pygame.init()
        self.display_surface = screen

        self.logros = Logros(self.display_surface)
        self.center_of_screen = self.display_surface.get_rect().center
        self.x_centroScreen, self.y_centroScreen = self.center_of_screen
        
        self.level = YSortCameraGroup()

        # Cargamos imagen de la barra
        self.barra_vida= pygame.image.load("graphics/elementos_graficos/barra.png").convert_alpha()
        self.barra_vida = pygame.transform.scale(self.barra_vida, (86,23))

        self.barra_vida_rect= self.barra_vida.get_rect()
        self.bar_x = 0
        self.bar_y = 0
        self.flag = False

        self.barra_vida_relleno = (self.bar_x+17,(self.bar_y+self.barra_vida_rect.height//2))
        self.barra_max_ancho = 62 #pixeles
        self.barra_alto = 2

    # Función para dibujar la barra de vida
    def Mostrar_vida(self, vida_actual, vida_completa, objetoEntity):
        #dibuja la barra de vida en la pantalla
        self.objetoEntity = objetoEntity

        self.display_surface.blit(self.barra_vida,(self.bar_x, self.bar_y))
        
        resp = self.level.obtener_posRespecto_camara(self.objetoEntity)
        pos1 = (self.objetoEntity.rect.x,self.objetoEntity.rect.y)

        self.objetoEntity.updateMess(self.display_surface)
        
        if vida_actual <= 10:
            if self.flag == False:
                self.objetoEntity.printMess("Tienes queda poca vida: "+ str(int(vida_actual)), 800)
                self.flag = True
        else:
            self.objetoEntity.deleteMessTime(3000)
            self.flag = False
        if vida_actual <= 0:
            self.objetoEntity.deleteMess()
    
            self.Muerte()
            self.objetoEntity.stop()
           
    
        posicion_a_seguir = resp[0], resp[1]
        # Posicion de la barra, la misma en x que la imagen pero más arriba
        self.bar_x, self.bar_y = Movimiento_suave(square_x=pos1[0]-posicion_a_seguir[0], square_y=pos1[1]-posicion_a_seguir[1], 
        bar_x=self.bar_x, bar_y=self.bar_y)

        ##colocamos dimenciones en pixeles para la barra:
        self.barra_vida_relleno = (self.bar_x+17,(self.bar_y+self.barra_vida_rect.height//2))

        current_health_ratio = vida_actual/vida_completa
        ancho_actual_barra = self.barra_max_ancho * current_health_ratio #regla de 3
        vida_barra_rect = pygame.Rect(self.barra_vida_relleno, (ancho_actual_barra,self.barra_alto))
        pygame.draw.rect(self.display_surface,'#FF2D2D', vida_barra_rect)
        
        pygame.display.update()

    def Muerte(self,size= [settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT], muerto=False):
        
        pygame.display.update()
        pygame.mixer.music.fadeout(500)
        
        fontsito = pygame.font.Font('graphics/font/joystix.ttf', 20)  

        menu_text = fontsito.render("Haz Muerto", True, "red")
        menu_rect = menu_text.get_rect(center=(size[0]/2, size[1]/10))

        boton=pygame.image.load("graphics/elementos_graficos/button.png")
        boton=pygame.transform.scale(boton,(240,90))

        fondo = pygame.image.load("graphics/elementos_graficos/fondosgenerico.png")

        fondo = pygame.transform.scale(fondo, (size[0], size[1]))

        Reiniciar = Button(image=boton, pos=(size[0]//2, 150),text_input="Reiniciar",font=fontsito,base_color="#7467F2",hovering_color="#F13816")

        salir_botton = Button(image=boton, pos=(size[0]//2, 250),text_input="Salir",font=fontsito,base_color="#7467F2",hovering_color="#F13816")
        
        
        while True:
            

            self.display_surface.blit(fondo, (0,0))
            self.display_surface.blit(menu_text, menu_rect)

            Reiniciar.cargar(self.display_surface)
            Reiniciar.cambiar_color(pygame.mouse.get_pos())

            salir_botton.cargar(self.display_surface)
            salir_botton.cambiar_color(pygame.mouse.get_pos())
            #!dammmm
            self.logros.updateNota()   
            events = pygame.event.get()
                
            for event in events:

                if event.type == pygame.QUIT:
                        respuesta = messagebox.askyesno("Precaución", "Se perderan los avances de este nivel. ¿Estás seguro?")
                        if respuesta:
                            # Acción a realizar si se confirma
                            print("Confirmado")
                            pygame.quit()
                            sys.exit()
                        else:
                            # Acción a realizar si se cancela
                            print("Cancelado")

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        
                        Reiniciar.click(self.display_surface)
                        pygame.mixer.music.unpause()
                        break

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if Reiniciar.checkForInput(pygame.mouse.get_pos()):

                        Reiniciar.click(self.display_surface)
                        pygame.mixer.music.play()
                        self.logros.agregar_logro("B3")
                        

                    elif salir_botton.checkForInput(pygame.mouse.get_pos()):
                        salir_botton.click(self.display_surface)
                        pygame.quit()
                        sys.exit()
                        
            pygame.display.update()

            clock.tick(60)


