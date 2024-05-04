import pygame, settings
from GUI.button import Button
from settings import *
from DB import validar

class Mezcladora():
    def __init__(self,screen, instrumentos, player, conexion, cursor): #= pygame.display.set_mode((settings.SCREEN_WIDTH,settings.SCREEN_HEIGHT))
        #self.lista_consumir = lista
        self.mezcladora = True
        self.screen = screen
        self.instrumentos = instrumentos
        self.player = player
        self.conexion = conexion
        self.cursor = cursor
              
    def mostrar_menu_mezcladora(self):
        
        self.fontsito = pygame.font.Font('graphics/font/joystix.ttf', 20)
        
        boton_regresar = Button(image=settings.botonRegresar, pos=(200,600),text_input="", font=self.fontsito,
                             base_color="#4D4D5C", hovering_color="#75E2EC")

        boton_mezclar = Button(image=settings.generalButton, pos=(SCREEN_WIDTH/2,500), text_input="Mezclar", font=self.fontsito,
                             base_color="#4D4D5C", hovering_color="#75E2EC")
        
        #Texto menu de instrumentos
        mezcladora_text = self.fontsito.render("Menu de mezcladora", True, "white") 
        mezcladora_rect = mezcladora_text.get_rect(center=(settings.SCREEN_WIDTH/2, settings.SCREEN_HEIGHT/11))

        fondo = pygame.image.load("graphics/elementos_graficos/fondosgenerico.png")
        fondo = pygame.transform.scale(fondo, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

        archivo_img = pygame.image.load("graphics/elementos_graficos/foldermusica.png")
        archivo_img = pygame.transform.scale(archivo_img,(50,50))

        archivo_img2 = pygame.image.load("graphics/elementos_graficos/foldermusica.png")
        archivo_img2 = pygame.transform.scale(archivo_img2,(50,50))

        #Cosas para mezclar
        mezcladora_costo = 1
        permiso_mezcladora = False
        pila_img = pygame.image.load("graphics/items/bateria.png")
        pila_img = pygame.transform.scale(pila_img,(50,50))
        pila_text = self.fontsito.render("x"+str(mezcladora_costo), True, "white")

        renderT = None

        while self.mezcladora:
            self.screen.fill((50,50,50))
            self.screen.blit(fondo,(0,0))

            self.screen.blit(mezcladora_text, mezcladora_rect)

            self.screen.blit(archivo_img,(300,200))
            self.screen.blit(archivo_img2,(300,300))

            self.screen.blit(pila_img,(SCREEN_WIDTH/2,550))
            self.screen.blit(pila_text,(600,575))
            boton_regresar.cargar(self.screen)

            boton_mezclar.cargar(self.screen)
            boton_mezclar.cambiar_color(pygame.mouse.get_cursor())



            if renderT is not None:
                self.screen.blit(renderT, rect)

            events = pygame.event.get()

            for event in events:

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if boton_regresar.checkForInput(pygame.mouse.get_pos()):
                        boton_regresar.click(self.screen)
                        self.mezcladora = False
                        return self.mezcladora

                        #Accion para entrar al menu Mezcladora
                    if boton_mezclar.checkForInput(pygame.mouse.get_pos()):
                        if mezcladora_costo <= self.player.items_num[0] and permiso_mezcladora == False:
                            constante = self.player.items_num[0] - mezcladora_costo
                            self.player.items_num[0] = constante
                            permiso_mezcladora = True
                            validar.insertar_items(self.player.items_num, self.conexion, self.cursor)
                        else:
                            #print("Necesitas mas items para usar la mezcladora")
                            text_no_mezcladora = "No se tienen suficientes para usar la mezcladora"
                            textR = pygame.font.Font("graphics/font/joystix.ttf", 15)
                            renderT = textR.render(text_no_mezcladora, True, (255,0,0))
                            rect = renderT.get_rect(center=(SCREEN_WIDTH//2, 150))
                        
                        if permiso_mezcladora == True:
                            text_mezcladora = "Se ha mezclado algo"
                            textR = pygame.font.Font("graphics/font/joystix.ttf", 15)
                            renderT = textR.render(text_mezcladora, True, (255,0,0))
                            rect = renderT.get_rect(center=(SCREEN_WIDTH//2, 150))
                        else:
                            #print("Necesitas mas items para usar la mezcladora")
                            text_no_mezcladora = "No se tienen suficientes para usar la mezcladora"
                            textR = pygame.font.Font("graphics/font/joystix.ttf", 15)
                            renderT = textR.render(text_no_mezcladora, True, (255,0,0))
                            rect = renderT.get_rect(center=(SCREEN_WIDTH//2, 150))
                    
            pygame.display.update()
