


class Hospital:
    def __init__(self, mundoConfig, enfermedadConfig):
        self.MundoConfig = mundoConfig
        self.EnfermedadConfig = enfermedadConfig
        self.capacidad = self.MundoConfig.CAPACIDAD_HOSPITALARIA
        self.ocupacion = 0
        self.individuos = []



    def ingresar(self, pygame, individuo, pos, dia):
        if (dia - individuo.diaInfeccion) < self.EnfermedadConfig.DIAS_DETECTAR_ENFERMEDAD:
            return False
        if self.ocupacion < self.capacidad:
            self.individuos.append(pos)
            self.ocupacion += 1
            individuo.hospitalizar(pygame)
            return True
        else:
            return False

    def darAlta(self, pygame, pos):
        for i in self.individuos:
            if i == pos:
                self.individuos.remove(i)
                if self.ocupacion > 0:
                    self.ocupacion -= 1
                break

    def disponible(self):
        if self.ocupacion < self.capacidad:
            return True
        else:
            return False