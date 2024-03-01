from settings import *

class Logros():
    def __init__(self, screen):
        self.screen = screen
        self.logros_desbloqueados = set()

        #cositas para los mensajes
        self.fondoMensaje = pygame.image.load("graphics/elementos_graficos/fondoMensaje.png")
        self.mess = "" 
        self.tiempoMess = 0
        self.tiempoInicio = 0

        self.wM = 0
        self.fA = 0
        self.hM = 40 

        #cositas para las notas
        self.font = pygame.font.Font(None, 22)
        self.nota = ""
        self.tiempoInicioNota = 0
        self.tiempoNotaMill = 0
        self.text_surfaceNota = self.font.render("", True, (255, 255, 255))
        self.superficieNota = pygame.Surface((230,40))
        self.superficieNota.fill((0,0,0))
        self.wN = 0
        self.hN = 22
        self.cola = []

    def printNota(self,nota,milisegundos):
        if(self.nota==""):
            self.nota = nota
            self.tiempoInicioNota = pygame.time.get_ticks()
            self.tiempoNotaMill = milisegundos
            print("se ejecuta Printnota")
        else:
            self.cola.append([nota, milisegundos])
        self.text_surfaceNota = self.font.render(self.nota, True, (255, 255, 255))
        
    def updateMess(self,surface):
        text_surface = self.font.render(self.mess, True, (255, 255, 255))
        if pygame.time.get_ticks()-self.tiempoInicio>self.tiempoMess and self.tiempoMess>0:
            self.mess = ""
            text_surface = self.font.render(self.mess, True, (255, 255, 255))
        if self.mess != "":
            esperado = text_surface.get_width()+200
            esperadoFa = 255
        else:
            esperado = 0
            esperadoFa = 0
        dif = esperado-self.wM
        self.wM +=dif*0.2
        dif = esperadoFa-self.fA
        self.fA+=dif*0.2
        
        fondoMensajeMod = pygame.transform.scale(self.fondoMensaje, (int(self.wM), int(self.hM)))
        surface.blit(fondoMensajeMod, (SCREEN_WIDTH/2-self.wM//2,20))
        text_x = SCREEN_WIDTH/2 - text_surface.get_width()/2
        text_y = 33
        text_surface.set_alpha(self.fA)
        surface.blit(text_surface, (text_x, text_y))
        
    def updateNota(self):
        if pygame.time.get_ticks()-self.tiempoInicioNota>self.tiempoNotaMill and self.tiempoNotaMill>0:
            self.nota = ""
        
        if self.nota != "":
            esperado2 = self.text_surfaceNota.get_width()+20
        else:
            esperado2 = 0
            if len(self.cola)>0 and self.wN<2:
                colaData = self.cola.pop(0)
                self.printNota(colaData[0], colaData[1])

        dif = esperado2-self.wN
        self.wN +=dif*0.2

        fondoNota = pygame.transform.scale(self.superficieNota, (int(self.wN), int(self.hN)))
        fondoNota.fill((0,0,0))
        fondoNota.blit(self.text_surfaceNota, (10,fondoNota.get_rect().centery-self.text_surfaceNota.get_height()//2))

        self.screen.blit(fondoNota, (0,170))

        
    def printMessWithImage(self, mensaje, imagen_path, milisegundos):
        """
        Muestra un mensaje junto con una imagen al principio.
        :param mensaje: Texto del mensaje.
        :param imagen_path: Ruta de la imagen a mostrar.
        :param milisegundos: Duración del mensaje en milisegundos.
        """
        # Cargar la imagen
        try:
            self.image = pygame.image.load(imagen_path)
        except pygame.error as e:
            print("Error al cargar la imagen:", e)
            return

        # Redimensionar la imagen a un tamaño específico
        imagen_ancho, imagen_alto = 50, 50  # Ajusta el tamaño según tus necesidades
        self.image = pygame.transform.scale(self.image, (imagen_ancho, imagen_alto))

        # Llamar a la función original para mostrar el mensaje
        self.printMess(mensaje, milisegundos)

    def updateMessWithImage(self):

        # Llamar a la función original para actualizar el mensaje
        self.updateMess()

        # Si hay una imagen, dibujarla al principio del mensaje
        if self.image:
            x_image = SCREEN_WIDTH // 2 - self.wM // 2 - 60  # Ajusta la posición según tus necesidades
            y_image = 20
            self.screen.blit(self.image, (x_image, y_image))
    
    def agregar_logro(self, logro):
        self.printNota(f"Logro desbloqueado: {logros_data[logro]['nombre']} - {logros_data[logro]['descripcion']}", 3000)
        self.logros_desbloqueados.add(logro)
        print(f"Logro desbloqueado: {logros_data[logro]['nombre']} - {logros_data[logro]['descripcion']}")
        
        