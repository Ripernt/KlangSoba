import pygame
import sys


# Bucle principal
def main():
    # Inicializar Pygame
    pygame.init()

    # Definir colores
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

    # Configuración de la ventana
    WIDTH, HEIGHT = 800, 600
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Cubo Músico")

    # Cargar música predeterminada
    pygame.mixer.music.load("audio/attack/i-see-clouds-171354.mp3")

    # Cargar música personalizada
    musica_personalizada = pygame.mixer.Sound("audio/bass-loops-006-with-drums-long-loop-120-bpm-6111.mp3")

    # Inicializar variables
    x, y = 50, 50
    velocidad = 5

    # Coordenadas de la zona con color diferente
    zona_x, zona_y, zona_ancho, zona_alto = 300, 200, 500, 400

    # Estado de la zona (True si el cubo está en la zona, False si está fuera)
    en_zona = False

    pygame.mixer.music.play(-1)  # Repetir música predeterminada indefinidamente


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Mover el cubo
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and x > velocidad:
            x -= velocidad
        if keys[pygame.K_RIGHT] and x < WIDTH - 50 - velocidad:
            x += velocidad
        if keys[pygame.K_UP] and y > velocidad:
            y -= velocidad
        if keys[pygame.K_DOWN] and y < HEIGHT - 50 - velocidad:
            y += velocidad

        # Verificar si el cubo está en la zona
        if zona_x < x < zona_x + zona_ancho and zona_y < y < zona_y + zona_alto:
            if not en_zona:
                en_zona = True
                pygame.mixer.music.stop()
                musica_personalizada.play(-1)
        else:
            if en_zona:
                en_zona = False
                musica_personalizada.stop()
                pygame.mixer.music.play(-1)  # Repetir música predeterminada

        # Limpiar la pantalla
        win.fill(BLACK)

        # Dibujar la zona con color diferente
        pygame.draw.rect(win, RED, (zona_x, zona_y, zona_ancho, zona_alto))

        # Dibujar el cubo
        pygame.draw.rect(win, WHITE, (x, y, 50, 50))

        # Actualizar la pantalla
        pygame.display.update()

# Ejecutar el juego
if __name__ == "__main__":
    main()



