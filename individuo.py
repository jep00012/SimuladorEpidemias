import random

class Individuo:
    def __init__(self, pygame, mundoConfig, enfermedadConfig, individuoConfig):
        self.MundoConfig = mundoConfig
        self.EnfermedadConfig = enfermedadConfig
        self.IndividuoConfig = individuoConfig
        if random.random() < self.MundoConfig.PORCENTAJE_VACUNADOS:
            self.vacunado = True
        else:
            self.vacunado = False

        if random.random() < self.MundoConfig.PORCENTAJE_USO_MEDIAS_HIGIENICAS:
            self.medidasHigiene = True
        else:
            self.medidasHigiene = False

        self.estado = self.IndividuoConfig.Estado[4]
        self.imagen = pygame.image.load(self.estado)
        self.diaFinInfectado = 7
        self.diaFinInmunidad = 0
        self.diaInfeccion = 0
        self.velocidad = [random.randint(-2, 3), random.randint(-2, 3)]
        self.cuadrado = self.imagen.get_rect()
        self.cuadrado.move_ip(random.randint(0, self.MundoConfig.ANCHO), random.randint(0, self.MundoConfig.ALTO))



    def cruceInfectado(self, pygame, individuo, dia):
        if individuo.estado == self.IndividuoConfig.Estado[0] and self.estado == self.IndividuoConfig.Estado[4] and not self.vacunado:
            if self.medidasHigiene:
                if random.random() <= (self.EnfermedadConfig.TASA_CONTAGIO - (self.EnfermedadConfig.TASA_CONTAGIO * self.MundoConfig.EFICACIA_MEDIDAS_HIGIENICAS)):
                    self.imagen = pygame.image.load(self.IndividuoConfig.Estado[0])
                    self.estado = self.IndividuoConfig.Estado[0]
                    self.diaFinInfectado = dia + (random.randint(self.EnfermedadConfig.DIAS_RECUPERACION[0], self.EnfermedadConfig.DIAS_RECUPERACION[1]))
                    if random.random() <= self.EnfermedadConfig.TASA_MORTALIDAD:
                        self.imagen = pygame.image.load(self.IndividuoConfig.Estado[3])
                        self.estado = self.IndividuoConfig.Estado[3]
                        self.velocidad = [0, 0]
            else:
                if random.random() <= self.EnfermedadConfig.TASA_CONTAGIO:
                    self.imagen = pygame.image.load(self.IndividuoConfig.Estado[0])
                    self.estado = self.IndividuoConfig.Estado[0]
                    self.diaFinInfectado = dia + (random.randint(self.EnfermedadConfig.DIAS_RECUPERACION[0], self.EnfermedadConfig.DIAS_RECUPERACION[1]))
                    if random.random() <= self.EnfermedadConfig.TASA_MORTALIDAD:
                        self.imagen = pygame.image.load(self.IndividuoConfig.Estado[3])
                        self.estado = self.IndividuoConfig.Estado[3]
                        self.velocidad = [0, 0]


    def comprobarRecuperado(self, pygame, dia):
        if  self.estado == self.IndividuoConfig.Estado[0] and self.diaFinInfectado <= dia:
            self.imagen = pygame.image.load(self.IndividuoConfig.Estado[1])
            self.estado = self.IndividuoConfig.Estado[1]
            self.diaFinInmunidad = dia + (random.randint(self.EnfermedadConfig.DIAS_INMUNIDAD[0], self.EnfermedadConfig.DIAS_INMUNIDAD[1]))
        if self.estado == self.IndividuoConfig.Estado[2] and self.diaFinInfectado <= dia:
            self.imagen = pygame.image.load(self.IndividuoConfig.Estado[1])
            self.estado = self.IndividuoConfig.Estado[1]
            self.velocidad = [random.randint(-2, 3), random.randint(-2, 3)]
            self.diaFinInmunidad = dia + (random.randint(self.EnfermedadConfig.DIAS_INMUNIDAD[0], self.EnfermedadConfig.DIAS_INMUNIDAD[1]))
        if self.estado == self.IndividuoConfig.Estado[1] and self.diaFinInmunidad <= dia:
            self.imagen = pygame.image.load(self.IndividuoConfig.Estado[4])
            self.estado = self.IndividuoConfig.Estado[4]

    def hospitalizar(self, pygame):
        self.imagen = pygame.image.load(self.IndividuoConfig.Estado[2])
        self.estado = self.IndividuoConfig.Estado[2]
        self.velocidad = [0, 0]
