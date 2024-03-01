from DB.conectar import conectar

def obtenerDataJugador(correo, conexionR=None, cursorR=None):
    if conexionR is None:
        conexion = conectar.conectar()
        cursor = conexion.cursor()
    else:
        conexion = conexionR
        cursor = cursorR
        

    arr = []

    query = "select * from usuario where usr_correo = %s"
    cursor.execute(query,[correo])
    resultado = cursor.fetchone()
    arr.extend(resultado)
    #correo = arr[0]


    """query = "select nvl_id, grd_tiempo from guardado where usr_id = %s"
    cursor.execute(query,[resultado[0]])
    resultado = cursor.fetchone()
    #obtineee el nivel y el tiempo
    if resultado is None:
        conectar.insertar_informacion([arr[0],0,0],cursorR,conexionR)
        arr.extend([0, 0])
    else:
        arr.extend(resultado)

    query = "select ani_id, alm_capturados, nvl_id from almanaque where usr_id = %s"
    cursor.execute(query,[arr[0]])
    resultado = cursor.fetchall()

    if resultado is not None:
        arr.append(resultado)
        # conectar.insertar_informacion_almanaque([arr[0],0,0,])
    else:
        arr.extend([])"""


    if conexionR is None:
        cursor.close()
        conexion.close()
    return arr