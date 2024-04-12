import threading
import numpy as np

class Datos:
    def __init__(self, individuoConfig):
        self.contadores = np.zeros((6, 1))
        self.lock = threading.Lock()
        self.IndividuoConfig = individuoConfig

    def actualizar(self, poblacion, dia):
        with self.lock:
            sanos, infectados, recuperados, hospitalizados, fallecidos = 0, 0, 0, 0, 0
            for i in range(len(poblacion)):
                if poblacion[i].estado == self.IndividuoConfig.Estado[4]:
                    sanos += 1
                elif poblacion[i].estado == self.IndividuoConfig.Estado[0]:
                    infectados += 1
                elif poblacion[i].estado == self.IndividuoConfig.Estado[1]:
                    recuperados += 1
                elif poblacion[i].estado == self.IndividuoConfig.Estado[2]:
                    hospitalizados += 1
                elif poblacion[i].estado == self.IndividuoConfig.Estado[3]:
                    fallecidos += 1
            #añadir una nueva columna
            self.contadores = np.append(self.contadores, [[dia], [sanos], [infectados], [recuperados], [hospitalizados], [fallecidos]], axis=1)

    def getDatos(self):
        with self.lock:
            return self.contadores

    def getDatos1Dia(self, dia):
        with self.lock:
            return self.contadores[1, dia]

    def getPicoInfectados(self):
        with self.lock:
            return self.contadores[2].max()

    def getDiaPicoInfectados(self):
        with self.lock:
            return np.argmax(self.contadores[2])

    def getMediaInfectados(self):
        with self.lock:
            return np.mean(self.contadores[2])
