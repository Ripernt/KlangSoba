import re
#from secure.cifrado import Cifradito
from DB.Sesion import Sesion
#from main import iniciarSesion, registrarUsuario
from DB import conectar
from DB.playerBD import obtenerDataJugador
from settings import*
import requests
import pygame
import sys
from GUI.EntryS import Entry
from GUI.button import Button


#valida inicio de sesion
def validar(correo,contraseña,cursor,conexion):
    global s

    correo = correo.lower()
    print(correo)
    if correo == "" or contraseña == "":
        print("llene los campos")
    elif validar_correo(correo):
        print("El correo electrónico es válido.")
        buscarcor = encontrarUsuario(correo, conexion, cursor)
        
        if buscarcor:
            print("SE HA ENCONTRADO AL USUARIO")
            validarcontra = validarContraseña(correo,contraseña)
            if validarcontra:
                print("SE VALIDADO LA CONTRASEÑA ")
                s = Sesion(obtenerDataJugador(correo, conexion, cursor))
                return s
            else:
                s = "contraseña incorrecta"
        else:
            s = "Usuario no encontrado"
    else:
        s = "El correo electrónico no es válido."

    

        
#obtiene el objeto sesion
def responseI():
    return s


"""valida registro"""
def validarRegistro(usuario,correo,contraseña,confirmcontra, conexion, cursor):
    
    correo = correo.lower()
    # print(correo)
    if usuario == "" or correo == "" or contraseña == "" or confirmcontra == "":
        return "Rellene los campos"
    elif validar_correo(correo): 
        
        if contraseña == confirmcontra:

            if not encontrarUsuario(correo, conexion, cursor):
                    res = autentificarCorreoUsuario(correo, conexion, cursor)
                    print("se enviaa correo")
                    if res:
                    
                        registrarUsuario(usuario,correo, contraseña, conexion, cursor)
                        print("se ha registrado exitosamente")
                        return "OK"
                    else:
                        return "codigo incorrecto, vuelva a intentarlo"
            else:
                return "El correo ya existe"
        else:
            return "las contraseñas no coinciden"
    else:
        return "El correo no es valido"
    

"""ingresa info a la base de datos, registra"""
def registrarUsuario(usuario,correo, contraseña, conexionR = None, cursorR = None):
    query = "INSERT into usuario (usr_nombre, usr_contraseña, usr_correo, per_id) values (%s, %s, %s, %s);"
    #cifrado = Cifradito()
    #contraseña_cifrada = cifrado.encriptado(contraseña)
    valores= (usuario,contraseña,correo,1)
    #print(contraseña_cifrada)
    if conexionR is None:
        conexion = conectar.conectar()
        cursor = conexion.cursor()
    else:
        conexion = conexionR
        cursor = cursorR
    cursor.execute(query, valores)
    conexion.commit()
    if conexionR is None:
        cursor.close()
        conexion.close()

"""busca info a la base de datos, encuentra"""
def encontrarUsuario(correo, conexionR = None, cursorR = None):
    query = "select usr_correo from usuario where usr_correo = %s;"
    
    if conexionR is None:
        conexion = conectar.conectar()
        cursor = conexion.cursor()
    else:
        conexion = conexionR
        cursor = cursorR

    cursor.execute(query,[correo])
    resultado = cursor.fetchone()
    
    if conexionR is None:
        cursor.close()
        conexion.close()

    if resultado is not None:
        return True
    else:
        return False

"""una vez encontrado, compueba la contraseña"""
def validarContraseña(correo,contraseña, conexionR = None, cursorR = None):
    #cifrado = Cifradito()
    query = "select usr_contraseña from usuario where usr_correo = %s;"
    
    if conexionR is None:
        conexion = conectar.conectar()
        cursor = conexion.cursor()
    else:
        conexion = conexionR
        cursor = cursorR

    cursor.execute(query,[correo])
    resultado = cursor.fetchone()
    
    if conexionR is None:
        cursor.close()
        conexion.close()

    resultado[0]
    if contraseña == resultado[0]:
        return True
    else:
        return False

"""comprueba que la syntaxis sea de un correo"""
def validar_correo(correo):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'  # Expresión regular para validar el correo electrónico
    
    if re.match(patron, correo):
        return True
    else:
        return False
    
def enviarCorreo(correo):
    url = 'https://Francis.pythonanywhere.com/enviar_codigo'
    # Dirección de correo electrónico a la que se enviará el código
    # Realizar la solicitud POST al servidor Flask
    data = {'correo': correo}
    response = requests.post(url, json=data)

    # Verificar si la solicitud fue exitosa (código de respuesta 200)
    if response.status_code == 200:
        # Extraer el código de la respuesta en formato JSON
        return response.json()['codigo']
    else:
        return "Error"
    
"""codigo de verificacion"""   
def autentificarCorreoUsuario(correo, conexion, cursor):
    pygame.display.update()

    code = enviarCorreo(correo)
    print("enviaado a", correo)
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    pygame.mixer.music.pause()

    fontsito = pygame.font.Font('graphics/font/joystix.ttf', 20) 
    fontsito2 = pygame.font.Font('graphics/font/joystix.ttf', 15) 

    menu_text = fontsito.render("Valida tu Correo Electronico", True, "white")
    menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/10))

    mensaje = fontsito2.render("introduce el codigo enviado a: "+correo, True, "white")
    mensaje_rect = mensaje.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/10*3))

    fondo = pygame.image.load("graphics/elementos_graficos/shinee.png")
    fondo = pygame.transform.scale(fondo, (SCREEN_WIDTH, SCREEN_HEIGHT))

    entrada = Entry(screen, (400,300), 6, borderR=7, size=50,espacio=3)


    botonValidar = Button(image=generalButton, pos=(400,510),text_input="validar",font=fontsito,base_color="#4D4D5C",hovering_color="#75E2EC")
    botonReenviar= Button(image=generalButton, pos=(400,420),text_input="reenviar",font=fontsito,base_color="#4D4D5C",hovering_color="#75E2EC")

    tiempoReenvio = pygame.time.get_ticks()

    while True:
        screen.blit(fondo, (0,0))

        screen.blit(menu_text, menu_rect)
        screen.blit(mensaje, mensaje_rect)

        botonValidar.cargar(screen)
        botonValidar.cambiar_color(pygame.mouse.get_pos())

        botonReenviar.cargar(screen)
        botonReenviar.cambiar_color(pygame.mouse.get_pos())



        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                cursor.close()
                conexion.close()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if len(entrada.data) == entrada.digitos and botonValidar.checkForInput(pygame.mouse.get_pos()):
                    if entrada.data == code:
                        return True
                    else:
                        return False
        entrada.update(events)


        pygame.display.update()