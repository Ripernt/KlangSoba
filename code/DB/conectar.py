import mysql.connector
from DB.constants import *


#realiza la conexion


def conectar():
    try:
        bcdb = mysql.connector.connect(
            host=host,
            user=user,
            password= password, 
            database=db,
            port = port
        )
        return bcdb
    except mysql.connector.Error as error:
            print("Se produjo un error al conectar a la base de datos: {}".format(error))



def insertar_informacion(datos, cursor, conexion):
    try:
        # Conectar a la base de datos
       
        # Crear un cursor para ejecutar consultas

        query = f"SELECT * FROM guardado where usr_id = {datos[0]};"

        cursor.execute(query)

        res = cursor.fetchone()

        if res is None:
             query = f"insert into guardado (usr_id,nvl_id,grd_tiempo) values ({datos[0]},{datos[1]},{datos[2]});"
             cursor.execute(query)
        else:
            # Consulta de inserción
            consulta = f"UPDATE guardado SET nvl_id = {datos[1]}, grd_tiempo = {res[2]+datos[2]} WHERE usr_id = {datos[0]};"
            # Ejecutar la consulta con los datos proporcionados
            cursor.execute(consulta)

        # Confirmar los cambios en la base de datos
        conexion.commit()
             

        # Cerrar el cursor y la conexión
        
        print("Información insertada exitosamente.")
    except mysql.connector.Error as error:
        print("Se produjo un error al insertar la información: {}".format(error))
    
def insertar_informacion_almanaque(datos, cursor, conexion):
    try:
        # Conectar a la base de datos
        

        # Crear un cursor para ejecutar consultas

        query = f"SELECT * FROM almanaque where usr_id = {datos[0]} and ani_id = {datos[1]};"

        cursor.execute(query)
        print(type(cursor))

        res = cursor.fetchone()

        print(datos[0], datos[1], datos[2], datos[3])

        if res is None:
             query = f"insert into almanaque (usr_id,ani_id,alm_capturados, nvl_id) values ({datos[0]},{datos[1]},{datos[2]},{datos[3]});"
             cursor.execute(query)
             print("es None")
        else:
            # Consulta de inserción
            consulta = f"UPDATE almanaque SET alm_capturados = {res[2]+datos[2]}, nvl_id = {datos[3]} WHERE usr_id = {datos[0]} and ani_id = {datos[1]};"
            # Ejecutar la consulta con los datos proporcionados
            cursor.execute(consulta)

        # Confirmar los cambios en la base de datos
        conexion.commit()
             

        # Cerrar el cursor y la conexión

        print("Información insertada exitosamente.")
    except mysql.connector.Error as error:
        print("Se produjo un error al insertar la información: {}".format(error))