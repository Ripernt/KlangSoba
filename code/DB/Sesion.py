def calcular_dimensiones(arreglo):
    dimensiones = []
    while isinstance(arreglo, list):
        dimensiones.append(len(arreglo))
        arreglo = arreglo[0]
    return tuple(dimensiones)

class Sesion():
    def __init__(self, info):
        self.id = info[0]
        self.correo = info[3]
        self.password = info[2]

        self.nombre = info[1]
        self.permiso = info[4]
        """self.tiempoMin = info[6]
        

        an = info[7]
        self.animalList = []"""
        