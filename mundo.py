import random
import time
import pygame
from hospital import Hospital
from individuo import Individuo


class Mundo:
    def __init__(self, ejecutando, datos, mundoConfig, individuoConfig, enfermedadConfig):
        self.datos = datos
        self.MundoConfig = mundoConfig
        self.IndividuoConfig = individuoConfig
        self.EnfermedadConfig = enfermedadConfig
        self.jugando = ejecutando

    def setJugando(self, jugando):
        self.jugando = jugando

    def run(self):
        # Inicializamos el motor de juegos
        pygame.init()
        ventana = pygame.display.set_mode((self.MundoConfig.ANCHO, self.MundoConfig.ALTO))
        pygame.display.set_caption("Simulacion")

        # Inicializamos variables
        inicio = time.time()
        tiempoDia = time.time()
        dia = 0
        random.seed(self.MundoConfig.SEMILLA)

        # hospital
        hospital = Hospital(self.MundoConfig, self.EnfermedadConfig)

        # array de individuos
        poblacion = []
        for i in range(self.MundoConfig.POBLACION):
            # Crear individuo
            poblacion.append(Individuo(pygame, self.MundoConfig, self.EnfermedadConfig, self.IndividuoConfig))

        # individuo 0 infectado
        poblacion[0].imagen = pygame.image.load(self.IndividuoConfig.Estado[0])
        poblacion[0].estado = self.IndividuoConfig.Estado[0]

        # Pongo al individuo en el origen de coordenadas
        for i in range(self.MundoConfig.POBLACION):
            a1 = random.randint(0, self.MundoConfig.ANCHO)
            a2 = random.randint(0, self.MundoConfig.ALTO)
            poblacion[i].cuadrado.move_ip(0, 0)

        while self.jugando:
            # Compruebo si se ha pulsado alguna tecla
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    jugando = False

            # Muevo al individuo
            for i in range(self.MundoConfig.POBLACION):
                poblacion[i].cuadrado = poblacion[i].cuadrado.move(poblacion[i].velocidad)

            # Compruebo si el individuo llega a los límites de la ventana
            for i in range(self.MundoConfig.POBLACION):
                if poblacion[i].cuadrado.left < 0 or poblacion[i].cuadrado.right > ventana.get_width():
                    poblacion[i].velocidad[0] = -poblacion[i].velocidad[0]

                if poblacion[i].cuadrado.top < 0 or poblacion[i].cuadrado.bottom > ventana.get_height():
                    poblacion[i].velocidad[1] = -poblacion[i].velocidad[1]

            fin = time.time()
            # Compruebo si individuo choca con otro
            if fin - inicio > 0.0:
                for i in range(self.MundoConfig.POBLACION):
                    for j in range(self.MundoConfig.POBLACION):
                        if i != j:
                            if poblacion[i].cuadrado.colliderect(poblacion[j].cuadrado):
                                poblacion[i].cruceInfectado(pygame, poblacion[j], dia)

            # Compruebo si individuo entra en hospital
            for i in range(self.MundoConfig.POBLACION):
                if poblacion[i].estado == self.IndividuoConfig.Estado[
                    0] and hospital.disponible() and dia > self.MundoConfig.DIA_INICIO_HOSPITALIZACION and self.datos.getDatos1Dia(
                        dia) > self.MundoConfig.MINIMO_INDIVIDUOS_INFECTADOS_PARA_HOSPITALIZAR:
                    hospital.ingresar(pygame, poblacion[i], i, dia)

            ventana.fill((252, 243, 207))
            # Dibujo al individuo
            for i in range(self.MundoConfig.POBLACION):
                ventana.blit(poblacion[i].imagen, poblacion[i].cuadrado)

            # Se comprueba recuperaciones, dar de alta y se actualiza la grafica
            tiempoFdia = time.time()
            if tiempoFdia - tiempoDia > 0.5:
                dia += 1
                print("Dia: ", dia)
                tiempoDia = time.time()
                for i in range(self.MundoConfig.POBLACION):
                    poblacion[i].comprobarRecuperado(pygame, dia)
                    if poblacion[i].estado == self.IndividuoConfig.Estado[1]:
                        hospital.darAlta(pygame, i)
                self.datos.actualizar(poblacion, dia)
            # if dia == 200:
            #    jugando = False
            # Se simula una reinfeccion
            if dia % 50 == 0 and dia != 0:
                poblacion[0].imagen = pygame.image.load(self.IndividuoConfig.Estado[0])
                poblacion[0].estado = self.IndividuoConfig.Estado[0]
                poblacion[0].diaFinInfectado = dia + (random.randint(10, 15))
                poblacion[0].velocidad = [random.randint(-2, 3), random.randint(-2, 3)]

            pygame.display.flip()
            pygame.time.Clock().tick(60)

        pygame.quit()
