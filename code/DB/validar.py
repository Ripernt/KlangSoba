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


#valida registro
def validarRegistro(usuario,correo,contraseña,confirmcontra,lista,conexion, cursor):
    
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
                    
                        registrarUsuario(usuario,correo, contraseña, lista,conexion, cursor)
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
    

#busca info a la base de datos, encuentra
def encontrarUsuario(correo, conexionR = None, cursorR = None):
    global usu_correo
    usu_correo = correo
    query = "select usr_correo from usuario where usr_correo = %s;"
    #query2 = "select usr_id from usuario where usr_correo= %s;"    
    if conexionR is None:
        conexion = conectar.conectar()
        cursor = conexion.cursor()
    else:
        conexion = conexionR
        cursor = cursorR

        
    cursor.execute(query,[correo])
    resultado = cursor.fetchone()
    #cursor.execute(query2,[correo])
    #usu = cursor.fetchone()

    if conexionR is None:
        cursor.close()
        conexion.close()

    if resultado is not None:
        return True
    else:
        return False

#ingresa info a la base de datos, registra
def registrarUsuario(usuario,correo, contraseña,lista, conexionR = None, cursorR = None):
    global usu    

    query = "INSERT into usuario (usr_nombre, usr_contraseña, usr_correo, per_id) values (%s, %s, %s, %s);"
    query2 = "select usr_id from usuario where usr_correo = %s;"
    query3 = "INSERT INTO almanaque_item (usr_id, item_ite_id, ite_cantidad) values(%s,%s,%s);"
    query4 = "INSERT INTO almanaque_instrumento(ins_id,usr_id,alm_instrumento) values(%s,%s,%s);"

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
    cursor.execute(query2,[correo])
    usu = cursor.fetchone()

    
    #Insert bateria
    valores1 = (usu[0],1,lista[0])

    #Insert cables
    valores2 = (usu[0],3,lista[1])

    #Insert cuerdas
    valores3 = (usu[0],4,lista[2])

    #Insert madera
    valores4 = (usu[0],2,lista[3])

    cursor.execute(query3,valores1)
    cursor.execute(query3,valores2)
    cursor.execute(query3,valores3)
    cursor.execute(query3,valores4)
    conexion.commit()

    #valores5 = (1,usu[0])
    valores5 = (2,usu[0],1)
    valores6 = (3,usu[0],1)

    cursor.execute(query4,valores5)
    cursor.execute(query4, valores6)
    conexion.commit()
    
    if conexionR is None:
        cursor.close()
        conexion.close()


    
"""Insertar items"""
def insertar_items(lista,conexionR,cursorR):
    
    query = "Select usr_id from usuario where usr_correo =%s;"
    
    if conexionR is None:
        conexion = conectar.conectar()
        cursor = conexion.cursor()
    else:
        conexion = conexionR
        cursor = cursorR
    cursor.execute(query,[usu_correo])
    usu = cursor.fetchone()
    query2 = "Update almanaque_item set ite_cantidad = %s where usr_id = %s and item_ite_id = %s;"
    #Update bateria
    valores1 = (lista[0],usu[0],1)

    #Update cables
    valores2 = (lista[1],usu[0],3)

    #Updates cuerdas
    valores3 = (lista[2],usu[0],4)

    #Update madera
    valores4 = (lista[3],usu[0],2)

    cursor.execute(query2,valores1)
    cursor.execute(query2,valores2)
    cursor.execute(query2,valores3)
    cursor.execute(query2,valores4)
    conexion.commit()
    
    if conexionR is None:
        cursor.close()
        conexion.close()

def instrumento_piano(piano,conexionR,cursorR):
    query = "Select usr_id from usuario where usr_correo =%s;"
    query2 = "Update almanaque_instrumento set alm_instrumento = %s where usr_id = %s and ins_id = %s;"


    if conexionR is None:
        conexion = conectar.conectar()
        cursor = conexion.cursor()
    else:
        conexion = conexionR
        cursor = cursorR

    cursor.execute(query,[usu_correo])
    usu = cursor.fetchone()
    
    valores = (piano[0],usu[0],2)
    valores2 = (piano[1],usu[0],3)

    cursor.execute(query2,valores)
    cursor.execute(query2,valores2)
    conexion.commit()

    if conexionR is None:
        cursor.close()
        conexion.close()

"""def instrumento_sintetizador(piano,conexionR,cursorR):
    query = "Select usr_id from usuario where usr_correo =%s;"
    query2 = "Update almanaque_instrumento set ins_id = %s where usr_id = %s;"


    if conexionR is None:
        conexion = conectar.conectar()
        cursor = conexion.cursor()
    else:
        conexion = conexionR
        cursor = cursorR

    cursor.execute(query,[usu_correo])
    usu = cursor.fetchone()
    
    valores = (piano[0],usu[0])

    cursor.execute(query2,valores)
    conexion.commit()

    if conexionR is None:
        cursor.close()
        conexion.close()"""



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
    url = 'https://carapia7.pythonanywhere.com/enviar_codigo'
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

def obtener_items(correo,conexionR, cursorR):
    listita = []
    corr = correo
    query = "select usr_id from usuario where usr_correo = %s;"

    query2 = "Select ite_cantidad from almanaque_item where usr_id = %s and item_ite_id=%s;"
    if conexionR is None:
        conexion = conectar.conectar()
        cursor = conexion.cursor()
    else:
        conexion = conexionR
        cursor = cursorR

    cursor.execute(query,[corr])
    usu = cursor.fetchone()


    valores = (usu[0],1) 
    valores2 = (usu[0],3) 
    valores3= (usu[0],4)
    valores4 = (usu[0],2) 

    cursor.execute(query2,valores)
    a = cursor.fetchone()
    cursor.execute(query2,valores2)
    b = cursor.fetchone()
    cursor.execute(query2,valores3)
    c = cursor.fetchone()
    cursor.execute(query2,valores4)
    d = cursor.fetchone()

    if conexionR is None:
        cursor.close()
        conexion.close()
        
    if a == None:
        a = (0,)
    if b == None:
        b = (0,)
    if c == None:
        c = (0,)
    if d == None:
        d = (0,)
    listita = [*a, *b, *c, *d]
    return listita


def obtener_instrumento_piano(correo,conexionR,cursorR):
    
    lista_instrumento = []

    query = "Select usr_id from usuario where usr_correo = %s"
    query2 = "Select alm_instrumento from almanaque_instrumento where usr_id = %s and ins_id = %s;"

    if conexionR is None:
        conexion = conectar.conectar()
        cursor = conexion.cursor()
    else:
        conexion = conexionR
        cursor = cursorR

    cursor.execute(query,[correo])
    usu = cursor.fetchone()

    valores = (*usu,2)
    valores1 = (*usu,3)
    cursor.execute(query2,valores)
    a = cursor.fetchone()
    cursor.execute(query2,valores1)
    b = cursor.fetchone()

    if conexionR is None:
        cursor.close()
        conexion.close()

    lista_instrumento = [*a,*b]

    return lista_instrumento









