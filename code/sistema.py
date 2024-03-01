from numpy import array, append, zeros, ones
from pygame import draw, time, Surface, SRCALPHA, transform, image
import pygame.gfxdraw as gfx

from random import randint
from math import sin, cos, radians, sqrt

from colores import rgba
import colores

class NegativeTime(Exception):
    def __init__(self, mensaje="Time cannot be negative"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)
class ImageNotLoaded(Exception):
    def __init__(self, mensaje="no image has been loaded to display, set an image using <set_surface>."):
        self.mensaje = mensaje
        super().__init__(self.mensaje)  
def distancia_euclidiana(punto1, punto2):
    """
    Calcula la distancia euclidiana entre dos puntos.

    Args:
        punto1 (tuple): Las coordenadas del primer punto.
        punto2 (tuple): Las coordenadas del segundo punto.

    Returns:
        float: La distancia euclidiana entre los dos puntos.
    """
    return sqrt(sum((p1 - p2) ** 2 for p1, p2 in zip(punto1, punto2)))


# Son particulas con fisicas y aspecto que se asemeja al del fuego
FUEGO = 0
# Son particulas que tienen fisicas y aspecto similar al del agua
AGUA = 1
# Son particulas con fisicas simples pero que pueden tomar el aspecto de una imagen, ademas de que tienen tiempo de vida definido
IMAGEN = 2
# Son particulas con fisicas simples pero que generan una nube similar al HUMO, ademas de que tienen tiempo de vida definido
HUMO = 3
# Son particulas que al contacto con plataformas pueden romperse en mas pedazos
ESCOMBRO = 4
# Son particulas con formas irregulares 
RESIDUO = 5
# Es la particula mas basica, un circulo de un solo color solido.
CLASICO = 7

class ParticleSystem:
    def __init__(self, typePart = CLASICO, gravity = 0, color = colores.ROJO, massPart = 1, airRes = 0, friction = 0):
        # 3 arreglos con indices correspondientes a cada particulas
        self.posiciones = []
        self.velocidades = []
        self.aceleraciones = []
        self.muertes = []
        self.deathTimes = []
        
        self.rangeDt = (0,0)
        self.rangeLife = (0,0)

        self.type = typePart
        self.gravity = gravity
        self.gravity_x = 0
        self.color = color
        self.massPart = massPart

        self.friction = friction
        self.airRes = airRes

        self.radius = 0
        self.set_radius(1)
        self.rand = False
        self.range = (0,10)
        
        self.image = None
            
        
        
        if(self.type == CLASICO or self.type == FUEGO):
            self.timeOfLife = 2000
        elif(self.type == RESIDUO or self.type == IMAGEN):
            self.timeOfLife = 3000
        elif(self.type == ESCOMBRO or self.type == AGUA):
            self.timeOfLife = -1
        elif self.type == HUMO:
            self.timeOfLife = 1000
            
        self.deathTime = 0
        
    def set_radius(self, radio_base):
        """establece el radio de las particulas

        Args:
            radio_base (int): el radio de referencia para todas las particulas
            range (tuple, optional): cada particula va a tener un radio aleatorio dentro de este rango en referencia al radio base. Defaults to (0,10).
            rand (bool, optional): si se establece en VERDADERO cada particula tendra su radio independiente, sino, todas las particulas tendran el mismo radio cumpliendo con el criterio del rango establecido. Defaults to False.
        """
        self.radius = radio_base
        self.surf = Surface((self.radius+5, self.radius+5), SRCALPHA)
        
        if self.type == HUMO:
            self.gravity = -200
            for i in range(self.radius+5):
                for j in range(self.radius+5):
                    w = self.surf.get_width()
                    h = self.surf.get_height()
                    dis_centro = distancia_euclidiana((i,j), (w//2+0.5, h//2+0.5))
                    rel = min(max(dis_centro/(w//2), 0), 1)
                    
                    
                    if(randint(0,100)<80):
                        self.surf.set_at([i,j], rgba(colores.GRIS, 30-rel*30))
    
    def set_time_of_life(self, time, range = [0,0]):
        """Recibe un tiempo de vida para la particula, todo tiempo de vida negativo hara que la particula
        viva indefinidamente

        Args:
            time (int): tiempo de vida en milisegundos
            range (list, optional): rango dentro del cual se generara un tiempo de vida aleatorio para cada particula partiendo del tiempo dado. Defaults to [0,0].
        """
        self.timeOfLife = -1 if time<0 else time
        self.rangeLife = range
    def set_death_time(self, time, range = [0,0]):
        """establece el tiempo de muerte, pasado el tiempo de vida, durante este lapso de tiempo la particula desaparecera con una transicion correspondiente a su tipo(definido por el atributo type)

        Args:
            time (int): tiempo de muerte en milisegundos
            range (list, optional): se le asignara un tiempo de muerte aleatorio dentro de este rango y en referencia el tiempo establecido como base. Defaults to [0,0].
        """
        if(time<0):
            raise NegativeTime()
        self.rangeDt = range
        self.deathTime = time
    def set_surface(self, direccion, size):
        self.image = image.load(direccion)
        self.image = transform.scale(self.image, size)
        
    def add_Particle(self, pos, velocidad = [0,0]):
        """añade una particula al sistema

        Args:
            pos (list): será la posicion de la particula en relacion al marco del sistema.
            velocidad (list, optional): será la velocidad inicial de la particula. Defaults to [0,0].
        """
        self.posiciones.append(pos)
        self.velocidades.append(velocidad)
        self.aceleraciones.append([0,0])
        self.muertes.append(time.get_ticks()+(10**10 if self.timeOfLife==-1 else self.timeOfLife) + randint(self.rangeLife[0],self.rangeLife[1]))
        self.deathTimes.append(self.deathTime+randint(self.rangeDt[0],self.rangeDt[1]))
    def remove_particle(self, index):
        self.posiciones.pop(index)
        self.velocidades.pop(index)
        self.aceleraciones.pop(index)
        self.muertes.pop(index)
    
    def apply_force(self, indexParticle, force, angle):
        """aplica una fuerza a una particula dado su indice y el vector de fuerza

        Args:
            indexParticle (int): el indice de la particula
            force (float): magnitud de la fuerza
            angle (float): angulo del vector respecto al eje positivo de las abscisas
        """
        acel = self.aceleraciones[indexParticle]
        acel[0]+= (force * cos(angle))/self.massPart
        acel[1]+= (force * sin(angle))/self.massPart
    def apply_force_comp(self, indexParticle, force_X, force_Y):
        """aplica una fuerza a una particula dado su indice y los componentes de la fuerza

        Args:
            indexParticle (nt): el indice de la particula
            force_X (float): componente x de la fuerza a aplicar
            force_Y (float): componente y de la fuerza a aplicar
        """
        acel = self.aceleraciones[indexParticle]
        acel[0]+=force_X/self.massPart
        acel[1]+=force_Y/self.massPart
    def gen_Particles_matrix(self, ancho, alto, separation_x, separation_y, center):
        """genera una matriz de particulas con el ancho y alto establecido en una posicion dada

        Args:
            ancho (int): ancho de la matriz (en particulas)
            alto (int): alto de la matriz (en particulas)
            separation_x (int): separacion entre el centro de cada particula en x (en pixeles)
            separation_y (int): separacion entre el centor de cada particula en y (en pixeles)
            center (list): posicion del centro de la matriz generada
        """
        for i in range(ancho):
            for j in range(alto):
                self.add_Particle([i*separation_x+center[0]-(ancho*separation_x)/2,j*separation_y+center[1]-(alto*separation_y)/2], [0,0])
    def gen_particles_square_explosion(self, num_particles, max_explosion_speed, center):
        """genera una explosion de particulas con forma de cuadrado

        Args:
            num_particles (int): numero de particulas que se generaran en la explosion
            max_explosion_speed (float): velocidad maxima a la que podrá iniciar una particula de la explosion
            center (list): posicion del centro de la explosion
        """
        for _ in range(num_particles):
            self.add_Particle(center.copy(),[randint(-max_explosion_speed,max_explosion_speed),randint(-max_explosion_speed,max_explosion_speed)])
    def gen_particles_circular_explosion(self, num_particles, max_explosion_speed, center):
        """genera una explosion de particulas con forma circular

        Args:
            num_particles (int): cantidad de particulas a generar
            max_explosion_speed (float): velocidad maxima a la que puede iniciar cada particula
            center (list): posicion del centro de la explosion
        """
        for _ in range(num_particles):
            angle = randint(0,360)
            magnitude = randint(-max_explosion_speed, max_explosion_speed)
            
            self.add_Particle(center.copy(),[magnitude*cos(radians(angle)), magnitude*sin(radians(angle))])
    def gen_particles_starry_explosion(self, num_particles, puntas, center, potencia = 1):
        angleInit = randint(0,360)
        for i in range(num_particles):
            angle = randint(0, 360)
            sep_vert = 360/(puntas)
            v = abs((angle+angleInit)%sep_vert-(sep_vert/2))
            fuerza = (v)/2+20 
            
            fuerza*=potencia* (randint(0,100)/100)
            
            self.add_Particle(center.copy(), [fuerza * cos(radians(angle)), fuerza * sin(radians(angle))])
    def gen_particles_reguilete_explosion(self, num_particles, puntas, center, factor=1, potencia = 1):
        angleInit = randint(0,360)
        for i in range(num_particles):
            angle = randint(0, 360)
            sep_vert = 360/(puntas)
            v = abs((angle+angleInit)%sep_vert-(sep_vert*factor))
            fuerza = (v)/2+20 
            
            fuerza*=potencia * (randint(50,100)/100)
            
            self.add_Particle(center.copy(), [fuerza * cos(radians(angle)), fuerza * sin(radians(angle))])

    def gen_particle_jet(self, num_particles, center, angle, rangeA, max_speed):
        for i in range(num_particles):
            sp = max_speed*randint(0,100)/100
            self.add_Particle(center.copy(), [sp*cos(radians(angle+randint(-rangeA, rangeA))), sp*sin(radians(angle+randint(-rangeA, rangeA)))])
        

            
            
                
    
    def update(self, dt):
        blackList = []
        for i, p in enumerate(self.posiciones):
            
            
            if(self.muertes[i]+self.deathTimes[i]<time.get_ticks()):
                blackList.append(i)
                
            acel = self.aceleraciones[i]
            vel = self.velocidades[i]

            # Aplicar resistencia del aire
            vel[0]*=1-self.airRes
            vel[0]*=1-self.airRes
            
            acel[1] += self.gravity
            acel[0] += self.gravity_x
            
            
            vel[0]+=acel[0]*dt
            vel[1]+=acel[1]*dt
            
            p[0]+=vel[0]*dt
            p[1]+=vel[1]*dt
            
            acel[0]=0
            acel[1]=0
        for index, i in enumerate(blackList):
            self.remove_particle(i-index)
            
    def draw(self, screen):
        for i, p in enumerate(self.posiciones):
            opacity = 255
            timeT = time.get_ticks()
            if(self.muertes[i]<timeT):
                d = timeT-self.muertes[i]

                opacity = int(round(255 * d/(self.deathTimes[i]+0.1)))
                opacity = 255-max(min(opacity, 255), 0)
                
                
            
            if self.type == CLASICO:
                gfx.aacircle(screen, int(round(p[0])), int(round(p[1])), self.radius, rgba(self.color, opacity))   
                gfx.filled_circle(screen, int(round(p[0])), int(round(p[1])), self.radius, rgba(self.color, opacity))  
            elif self.type == HUMO:
                img = self.surf

                img.set_alpha(opacity)
                
                rect = img.get_rect(center=(int(round(p[0])), int(round(p[1]))))
                screen.blit(img, rect)
            elif self.type == IMAGEN:
                if(self.image == None):
                    raise ImageNotLoaded()
                
                self.image.set_alpha(opacity)
                rect = self.image.get_rect(center=(int(round(p[0])), int(round(p[1]))))
                screen.blit(self.image, rect)