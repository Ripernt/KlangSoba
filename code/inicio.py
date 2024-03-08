import pygame ,sys

from tkinter import messagebox

from plataforma import Plataforma
import sistema
import colores
import settings


class Inicio:

    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()
        pygame.time.set_timer(pygame.USEREVENT + 1, 100)
        self.sistema_particulas = sistema.ParticleSystem(gravity=0, airRes=0.001, typePart=sistema.IMAGEN)
        self.sistema_particulas.set_radius(20)
        self.sistema_particulas.set_death_time(500, [0, 0])
        self.sistema_particulas.set_time_of_life(700, [0, 0])
        self.sistema_particulas.set_surface("graphics/papu/notas.png", [50, 50])
        self.sistema_particulas.gravity_x = -500

        self.block_x = 617
        self.block_y = 115
        self.block_width = 276
        self.block_height = 120
        self.mouse_over_block = False

        self.iniciarSesion= False
        
    def mostrar_imagen_atenuada(self, image, time, p1, pasos, notas=False):
        for i in range(0, 256, pasos):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.USEREVENT + 1 and notas:
                    self.sistema_particulas.gen_particle_jet(1, [self.screen.get_width() // 4 * 3, self.screen.get_height() // 2], 360, 50, 300)

            self.screen.fill((255, 255, 255))
            image.set_alpha(i)
            self.screen.blit(image, p1)

            if notas:
                self.sistema_particulas.update(0.016)
                self.sistema_particulas.draw(self.screen)

            pygame.display.flip()
            pygame.time.wait(2)

        timeIni = pygame.time.get_ticks()
        while pygame.time.get_ticks() - timeIni < time:
            self.screen.fill((255, 255, 255))
            self.screen.blit(image, p1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.USEREVENT + 1 and notas:
                    self.sistema_particulas.gen_particle_jet(1, [self.screen.get_width() // 4 * 3, self.screen.get_height() // 2], 360, 50, 300)

            if notas:
                self.sistema_particulas.update(0.016)
                self.sistema_particulas.draw(self.screen)
            pygame.display.flip()
            pygame.time.wait(2)

        for i in range(255, -1, -pasos):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.fill((255, 255, 255))
            image.set_alpha(i)
            self.screen.blit(image, p1)

            if notas:
                self.sistema_particulas.update(0.016)
                self.sistema_particulas.draw(self.screen)
            pygame.display.flip()
            pygame.time.wait(2)

        pygame.time.wait(300)

    def logos(self):

        size = [settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT]
        self.screen = pygame.display.set_mode(size)

        bioc = pygame.image.load("graphics/papu/bclogo.png")
        fasts = pygame.image.load("graphics/papu/logo-fs.gif")
        elmejorjuego = pygame.image.load("graphics/papu/spinelogo.gif")
        klangsoba = pygame.image.load("graphics/papu/ks (1).png")

        logos = [pygame.transform.scale(bioc, (bioc.get_width()//2,bioc.get_height()//2)), fasts, elmejorjuego, pygame.transform.scale(klangsoba, (klangsoba.get_width()//2,klangsoba.get_height()//2))]

        # ------------------------ carga las imagenes ------------------------

        self.logo_x = settings.SCREEN_WIDTH / 2
        self.logo_y = settings.SCREEN_HEIGHT / 2

        # Inicio with logos
        self.mostrar_imagen_atenuada(logos[1], 500, (self.logo_x - logos[1].get_width() / 2, self.logo_y - logos[1].get_height() / 2), 4)
        self.mostrar_imagen_atenuada(logos[2], 500, (self.logo_x - logos[2].get_width() / 2, self.logo_y - logos[2].get_height() / 2+40), 4)
        self.mostrar_imagen_atenuada(logos[0], 1000, (self.logo_x - logos[0].get_width() / 2, self.logo_y - logos[0].get_height() / 2), 2)
        self.mostrar_imagen_atenuada(logos[3], 1000, (self.logo_x - logos[3].get_width() / 2, self.logo_y - logos[3].get_height() / 2), 2, True)

    def inicio(self):
        from GUI.button import Button
        pantallaInicio = pygame.image.load("graphics/papu/ks-startScreen.png")

        brillo = pygame.image.load("graphics/papu/ks (1).png")
        brillo = pygame.transform.scale(brillo, (brillo.get_width()//200*99-4, brillo.get_height()//20*10+6))


        pygame.mixer.music.load('audio/King Crimson - 21st Century Schizoid Man - 8-bit Version [TubeRipper.com].ogg')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.4)

        fontsito = pygame.font.Font('graphics/papu/joystix.TTF', 20)
        self.screen.fill((50, 50, 50))

        menu_text = fontsito.render("klangosab", True, "white")
        menu_rect = menu_text.get_rect(center=(settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT / 10))


    
        iniciosesion = Button(image=settings.generalButton, pos=(self.logo_x-125, 620), text_input="Iniciar Sesion", font=fontsito, base_color="#4D4D5C",
                             hovering_color="#C6DF29")
        registro = Button(image=settings.generalButton, pos=(self.logo_x+125, 620), text_input="Registrarse", font=fontsito, base_color="#4D4D5C",
                          hovering_color="#DFAD29")
        
        chatKS = Button(image=settings.botonPurChat, pos=(1180, 670), text_input="CHAT", font=fontsito, base_color="#4D4D5C",
                          hovering_color="#C66FF1", link="https://roomy-invented-bank.glitch.me/")

        """ pantalla de inicio """
        suelo = Plataforma()
        self.flag = True

        while self.flag:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                        
            self.screen.blit(pantallaInicio, (0, 0))
            self.screen.blit(brillo, (368, 16))

            iniciosesion.cargar(self.screen)
            iniciosesion.cambiar_color(pygame.mouse.get_pos())

            registro.cargar(self.screen)
            registro.cambiar_color(pygame.mouse.get_pos())

            chatKS.cargar(self.screen)
            chatKS.cambiar_color(pygame.mouse.get_pos())

            mouse_x, mouse_y = pygame.mouse.get_pos()

            if self.block_x < mouse_x < self.block_x + self.block_width and self.block_y < mouse_y < self.block_y + self.block_height:
                mouse_over_block = True
            else:
                mouse_over_block = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    
                if event.type == pygame.USEREVENT + 1:
                    if mouse_over_block:
                        self.sistema_particulas.gen_particle_jet(3, [mouse_x, mouse_y], 360, 50, 300)


                if event.type == pygame.MOUSEBUTTONDOWN:

                    if iniciosesion.checkForInput(pygame.mouse.get_pos()):
                        
                        iniciosesion.click(self.screen)
                        pygame.mixer.music.stop()
                        self.flag = False
                        
                        return True
                    if registro.checkForInput(pygame.mouse.get_pos()):
                        registro.click(self.screen)
                        pygame.mixer.music.stop()
                        self.flag = False
                        
                        return False
                    
                    if chatKS.checkForInput(pygame.mouse.get_pos()):
                        chatKS.click(self.screen)

            self.sistema_particulas.update(0.016)
            self.sistema_particulas.draw(self.screen)

            self.screen.set_at([200, 200], colores.rgba(colores.ROJO, 0))

            pygame.draw.rect(self.screen, colores.CHOCOLATE, suelo.rect)

            pygame.display.update()
            dt = self.clock.tick(60) / 1000

            pygame.display.set_caption(f'fps: {round(self.clock.get_fps())}')

    
    
