import pygame
import sys
from time import time
from settings import *
from level import Level
from inicio import Inicio
from GUI.Pausa import PausaMenu
from DB import conectar as Conectar
from DB.conectar import *
from GUI.button import Button
from GUI.Entry import InputBox
from DB.validar import validar
from DB.Sesion import Sesion
from spritesheet_functions import SpriteSheet
import threading
from tkinter import messagebox
def main():

    conect = conectar.conectar()
    cursor = conect.cursor()
    cursor.execute("select * from usuario;")
    for x in cursor:
        print(x)
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.update()


    pygame.mixer.music.pause()
    
    fontsito = pygame.font.Font('graphics/font/joystix.ttf', 20) 

    screen.fill((50, 50, 50))

    menu_text = fontsito.render("Inicia Sesion con tu Fast-Stern ID", True, "white")
    menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/10))

    boton=pygame.image.load("graphics/elementos_graficos/button.png")
    boton=pygame.transform.scale(boton,(240,90))

    fondo = pygame.image.load("graphics/elementos_graficos/shinee.png")

    fondo = pygame.transform.scale(fondo, (SCREEN_WIDTH, SCREEN_HEIGHT))

    botoniniciar = Button(image=boton, pos=(400,500),text_input="Iniciar Sesion",font=fontsito,base_color="#4D4D5C",hovering_color="#75E2EC")

    cajaI = InputBox((200,200,400,32), "Correo", colorValue=[(0,0,0), (255,0,0)])
    cajaC = InputBox((200,300,400,32), "Contraseña", colorValue=[(0,0,0), (255,0,0)])


    renderT = None

    while True:
        screen.blit(fondo, (0,0))

        screen.blit(menu_text, menu_rect)
        
        #if renderT is not None:
            #self.screen.blit(renderT, rect)

        botoniniciar.cargar(screen)
        botoniniciar.cambiar_color(pygame.mouse.get_pos())


        cajaI.update(screen)
        cajaC.update(screen)

        for event in pygame.event.get():
            cajaI.handle_event(event)
            cajaC.handle_event(event)

            if event.type == pygame.QUIT:
                respuesta = messagebox.askyesno("Precaución", "Se perderan los avances de este nivel. ¿Estás seguro?")
                if respuesta:
                    # Acción a realizar si se confirma
                    print("Confirmado")
                    cursor.close()
                    conect.close()
                    pygame.quit()
                    sys.exit()
                else:
                    # Acción a realizar si se cancela
                    print("Cancelado") 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botoniniciar.checkForInput(pygame.mouse.get_pos()):
                    botoniniciar.click(screen)
                    correo = cajaI.text
                    contraseña = cajaC.text
                    #correo = "flores.solis.jared.mauricio@gmail.com"
                    #contraseña = "12345"
                    t1 = threading.Thread(target= validar.validar,args=(correo,contraseña,cursor,conect))
                    t1.start()
                    t1.join()
                    response = validar.responseI()
                    if isinstance(response, Sesion):
                        return response
                    else:
                        textR = pygame.font.Font("Fonts/static/RobotoMono-Regular.ttf", 15)
                        renderT = textR.render(response, True, (255,0,0))
                        rect = renderT.get_rect(center=(SCREEN_WIDTH//2, 400))

        pygame.display.update()

if __name__ == "__main__":
    main()