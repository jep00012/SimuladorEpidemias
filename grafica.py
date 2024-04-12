import numpy as np
from matplotlib import pyplot as plt

class Grafica:
    def __init__(self, ejecutando, datos):
        self.datos = datos
        self.x_values = []
        self.y_values = [[] for _ in range(5)]  # Lista de listas para almacenar los datos
        self.ejecutando = ejecutando

        # Configuración de la gráfica
        plt.ion()  # Modo interactivo
        self.figure, self.ax = plt.subplots()
        self.lines = [
            self.ax.plot(self.x_values, y_values, label=label, color=color)[0]
            for y_values, label, color in
            zip(self.y_values, ["Sanos", "Infectados", "Inmunizados", "Hospitalizados", "Fallecidos"],
                ["green", "red", "blue", "orange", "gray"])
        ]
        self.ax.set_xlabel('Nº de individuos')
        self.ax.set_ylabel('Días')
        self.ax.set_title('Gráfico en tiempo real')
        #colocar leyenda fuera del grafico
        self.ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))


    def setEjecutando(self, ejecutando):
        self.ejecutando = ejecutando
    def update_plot(self):
        while self.ejecutando:
            data = self.datos.getDatos()
            x = data[0]  # La primera fila es el eje x
            y = data[1:]  # Las siguientes filas son los datos

            self.x_values = x

            for i, line in enumerate(self.lines):
                line.set_xdata(x)
                line.set_ydata(y[i])

            self.ax.relim()
            self.ax.autoscale_view()

            plt.pause(0.5)  # Actualizar cada segundo