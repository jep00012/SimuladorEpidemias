# SIMULACIÓN DE EPIDEMIAS
A continución se detallará como funciona la simulación en cuanto al código se refiere, la aplicación está construida en python
## UTILIDADES
Primero explicaremos las variables globales que utilizamos para las ejecuciones, es decir, parámetros que se establecen antes de iniciar la simulación y que condicionan esto. Primero tendremos un archivo con tres clases de configuración para el VIRUS, los INDIVIDUOS y el MUNDO.
Este código se encuentra en el archivo 'utilidades.py' y estos son los parámetros que tenemos por defecto y mas tarde veremos como modificarlas.
```
class MundoConfig:  
  ANCHO = 1240  //Ancho de la ventana
  ALTO = 1080  //Alto de la ventana
  SEMILLA = 766569  //Semilla para generación de valores aleatorios
  POBLACION = 200  //Número de individuos
  CAPACIDAD_HOSPITALARIA = 10  //Capacidad de individuos simultaneos en hospitales
  DIA_INICIO_HOSPITALIZACION = 10  //Día de la epidemia en la que se activa el sistema sanitario
  MINIMO_INDIVIDUOS_INFECTADOS_PARA_HOSPITALIZAR = 11  //Mínimo de individuos infectados para poner en marcha los hospitales
  PORCENTAJE_USO_MEDIAS_HIGIENICAS = 0.5  //Porcentaje de la población que utiliza las medidas higiénicas 
  EFICACIA_MEDIDAS_HIGIENICAS = 0.3 //Porcentaje en el que pueden evitar la infección 
  PORCENTAJE_VACUNADOS = 0.2 //Porcentaje de la población que recibe la vacuna 
  
  //Toda la configuración del individuo es un enum con las imágenes para las bolitas
class IndividuoConfig:  
  INFECTADO = 0  
  RECUPERADO = 1  
  HOSPITALIZADO = 2  
  FALLECIDO = 3  
  SANO = 4  
  
  Estado = {  
        INFECTADO: "Infectado.png",  
        RECUPERADO: "Recuperado.png",  
        HOSPITALIZADO: "Hospitalizado.png",  
        FALLECIDO: "Fallecido.png",  
        SANO: "Sano.png"  
  }  
  
  
class EnfermedadConfig:  
  DIAS_RECUPERACION = [10, 15]  //Intervalo de días que tarda en recuperarse de la enfermedad
  TASA_MORTALIDAD = 0.02  //Porcentaje de los individuos infectados que fallecen
  TASA_CONTAGIO = 0.7  //Probabilidad con la que un individuo es infectado si se cruza con un infectado
  DIAS_DETECTAR_ENFERMEDAD = 4 //Días que tarda el hospital en saber si un individuo está infectado para poder ingresarlo 
  DIAS_INMUNIDAD = [20, 30] //Intervalo de días que puede durar la inmunidad del individuo
```

Estos parámetros podrán modificarse al inicio de la aplicación y se mostrará mas adelante cuando veamos el 'main.py'
## DATOS
Los datos que recogemos durante la ejecución y que pintamos en la gráfica deben estar almacenados en una clase y para esto creamos la clase Datos, la cual es la encargada de que accedamos correctamente a los datos. Para poder sincronizar la escritura y lectura de los datos debemos tener conocimientos de Sistemas Concurrentes ya que debemos establecer una política de exclusión mutua, es decir, mientras que alguien está accediendo a los datos para leer o escribir el otro espera hasta que se libere el recurso y entonces lo ocupa, esto lo hacemos mediante una libreria llamada 'threading' y el almacenamiento de los datos mediante otra librería llamada 'numpy' que nos permite un manejo de los Arrays más sencillo y eficiente.
### Constructor
Debemos pasarle la configuración del individuo ya que la necesitaremos más adelante.
```
class Datos:  
    def __init__(self, individuoConfig):  
        self.contadores = np.zeros((6, 1))  //Matriz datos x dias
        self.lock = threading.Lock()  //Semáforo exclusión mútua
        self.IndividuoConfig = individuoConfig //Configuración del indivíduo 
```
### Actualizar
La función actualizar será la encargada de recibir los datos y actualizar la matriz de contadores. Pasará por cada individuo de la población identificando su estado e incrementando el valor del contador de su estado correspondiente para más tarde introducirlos en la matriz junto al día correspondiente.
```
def actualizar(self, poblacion, dia):  
    Si el recurso está libre
        valores a 0
        Para cada individuo
            Si está sano  
                sanos += 1  
            O está infectado 
                infectados += 1  
            O está recuperado  
                recuperados += 1  
            O está hospitalizado 
                hospitalizados += 1  
            O ha fallecido  
                fallecidos += 1 
                 
         Añadir a la matriz los valores en el día correspondiente
```
### Resto de funciones
Además también tendremos las siguientes funciones que nos permitirán obtener los datos escritos siempre si el recurso está libre
```
getDatos(self) //Devuelve la matriz de datos
  
getDatos1Dia(self, dia) //Devuleve los datos de la matriz de un día concreto
  
getPicoInfectados(self) //Devuelve el pico de infectados registrado en la matriz 
  
getDiaPicoInfectados(self) //Devuelve día del pico de infectados registrado en la matriz 
  
getMediaInfectados(self) //Devuelve la media de infectados 
```

## Gráfica
Esta clase se encargará de acceder a los datos cada media segundo y pintar la gráfica, para esto usamos una librería llamada 'matplotlib' en la que se puede encontrar mucha documentación, video y estilos de gráficas que se pueden pintar. 
### Constructor
En este inicializaremos todos los parámetros de la gráfica y todas las carácterísticas que queramos que tenga, además de un parámetro para saber cuando detener su ejecución.
```
class Grafica:  
    def __init__(self, ejecutando, datos):  
        self.datos = datos  
	    self.ejecutando = ejecutando
		Resto de parámetros de la gráfica
```
### Actualizar gráfica
Esta función será un bucle infinito en el que, mientras que el parámetro de ejecución siga en verdadero, actualizaremos y pintaremos la gráfica cada medio segundo
```
def update_plot(self):  
    Mientras ejecutando sea verdadero
        Obetenemos los datos de la clase Datos
        Actualizamos la gráfica
        Pintamos la gráfica cada 0.5 seg
```

## Individuo
Esta clase controla todo lo que tiene que ver con el individuo, como puede ser su estado, dias de recuperación, dias de inmunidad, etc... También le pasamos las tres clases de configuración ya que se serán necesarias.
### Constructor
```
class Individuo:  
    def __init__(self, pygame, mundoConfig, enfermedadConfig, individuoConfig):  
        self.MundoConfig = mundoConfig  
        self.EnfermedadConfig = enfermedadConfig  
        self.IndividuoConfig = individuoConfig  
        self.vacunado = Aleatorio con probabilidad 'Porcentaje de vacunados'  
        self.medidasHigiene = Aleatorio con probabilidad 'Porcentaje de uso de medidas higiénicas'
		self.estado = self.IndividuoConfig.Estado[4]  
        self.imagen = pygame.image.load(self.estado)  
        self.diaFinInfectado = 7  
        self.diaFinInmunidad = 0  
        self.diaInfeccion = 0  
        self.velocidad = Aleatdef cruceInfectado(self, pygame, individuo, dia):
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
                        self.velocidad = [0, 0]orio en eje x e y  
        self.cuadrado = self.imagen.get_rect()  
        self.cuadrado.move_ip(Aleatorio)
```
Una de sus funciones principales será la que se invoque cuando tengamos un cruce entre dos individuos, momento en el cual veremos si el individuo con el que se cruza tiene el status de infectado y, en este caso de estarlo, se calcurá si se infecta o no.
```
def cruceInfectado(self, pygame, individuo, dia):  
    Si está sano y no vacudano y individuo está infectado  
        Si usa medidas higienicas  
            Si se contagia reduciendo la probabilidad por las medidas higienicas 
                self.imagen = Infectado
                self.estado = Infectado
                self.diaFinInfectado = Se calcula el día de recuperación (aleatorio entre los posibles)  
                Si el individuo muere (aleatorio con probabilidad de que muera)  
                    self.imagen = Fallecido 
                    self.estado = Fallecido
                    self.velocidad = 0  
        Si no usa medidas higienicas 
            Si se contagia según la probabilidad de contagio
                self.imagen = Infectado
                self.estado = Infectado
                self.diaFinInfectado = Se calcula el día de recuperación (aleatorio entre los posibles)  
                Si el individuo muere (aleatorio con probabilidad de que muera)  
                    self.imagen = Fallecido 
                    self.estado = Fallecido
                    self.velocidad = 0  
```

Otra función importante será en la que comprobaremos si el individuo se ha recuperado de su enfermedad para actuar en consecuencia
```
def comprobarRecuperado(self, pygame, dia):  
    Si está infectado y es su día de recuperación  
        self.imagen = Recuperado 
        self.estado = Recuperado
        self.diaFinInmunidad = Se calcula el dia de fin de inmunidad de manera aleatoria 
    Si está hospitalizado y es su día de recuperación  
        self.imagen = Recuperado  
        self.estado = Recuperado
        self.velocidad = nueva velocidad aleatoria
        self.diaFinInmunidad = Se calcula el dia de fin de inmunidad de manera aleatoria   
    Si está recuperado y es su día de fin de inmunidad  
        self.imagen = Sano  
        self.estado = Sano
```
La siguiente función es para cuando desde el hospital se nos indica que el individuo ha sido hospitalizado
```
def hospitalizar(self, pygame):  
    self.imagen = Hospitalizado
    self.estado = Hospitalizado
    self.velocidad = 0
```
## Hospital
En esta clase se simulará un hospital, es decir se tendrán individuos almacenados con una capacidad limitada. En este hospital los individuos no podrán morir ni infectar a otros individuos mientras que están en él, aunque no variará su tiempo de recuperación ni tendrán más inmunidad por ello
### Constructor
```
class Hospital:  
    def __init__(self, mundoConfig, enfermedadConfig):  
        self.MundoConfig = mundoConfig  
        self.EnfermedadConfig = enfermedadConfig  
        self.capacidad = self.MundoConfig.CAPACIDAD_HOSPITALARIA  
        self.ocupacion = 0  
        self.individuos = []
```
### Ingresar
Esta función nos permitirá ingresar en el hospital a un individuo, esta decisión se tomará en el mundo.
```
def ingresar(self, pygame, individuo, pos, dia):  
    Si no se ha detectado la enfemedad aún
        return False  
    Si tiene camas libres  
        self.individuos.append(pos)  
        self.ocupacion += 1  
        individuo.hospitalizar(pygame)  
        return True  
    Si no tiene camas libres
        return False
```
### Dar de alta
Esta función dará del alta del hospital al individuo, saldrá como recuperado y por lo tanto tendrá unos días de inmunidad.
```
def darAlta(self, pygame, pos):  
    Para cada individuo del hospital 
        Si es el individuo en pos 
            self.individuos.remove(i)  
            Si la ocupación no es menor que 0  
                self.ocupacion -= 1  
                break
```
## Mundo
El mundo es el encargado de sincronizar a los individuos con los hospitales, y llevar a cabo la simulación como la conocemos, ya que la otra parte es la encargada de recoger los datos y pintarlos. Para esto hemos utilizado una libreria llamada 'pygame' que nos simplifica la parte gráfica de la aplicación y del sistema de colisiones entre los individuos.
### Constructor
```
class Mundo:  
    def __init__(self, ejecutando, datos, mundoConfig, individuoConfig, enfermedadConfig):  
        self.datos = datos  
        self.MundoConfig = mundoConfig  
        self.IndividuoConfig = individuoConfig  
        self.EnfermedadConfig = enfermedadConfig  
        self.jugando = ejecutando
```
### Run
Esta funcíon será la encargada de producir el juego y de llevar a cabo todas las interacciones.
```
def run(self):
		pygame.init()
		ventana = Cofiguración ventana
		
		inicio= time()
		tiempoDia = time()
		dia = 0

		random.seed(semilla)

		hospital = Hospital()
		
		#array de individuos
		poblacion = []
		Para cada individuo
				Creamos cada individuo SANO
		Infectamos al primer individuo

		Para cada individuo
				Lo colocamos en el origen

		#Bucle de juego
		Mientras jugando
				Si dejamos de jugar
						jugando se pone false

				Para cada individuo
						Muevo al individuo a sus siguiente posición

				Para cada individuo
						Si da con un borde lateral
								cambio su velocidad en x a la opuesta
						Si da con un borde superior o inferior
								cambio su veolcidad en y a la opuesta

				Para cada individuo
						Para cada individuo
								Si no son el mismo
										Si chocan
												Llamo a individuo.cruceInfectado(individuo)

				Para cada individuo
						Si está infectado y hay espacio en el hospital y ha ha paso el dia de inicio de hospitacion y pasa el minimo de infectados
								Se ingresa al individuo

				Para cada individuo
						Pinto al individuo

				Si ha pasado un dia
						dia++
						Para cada individuo
								individuo.comprobarRecuperado()
								Si está hospitalizado
										hospital.darAlta()
						datos.actualizar()

				Si han pasado 50 dias
						reinfectar al primer individuo

		pygame.quit()
```

## Main
Como mencinamos anteriormente si necesitamos exclusión mutua en una de nuestras clases esto es debido a que tenemos dos partes del programa corriendo al mismo tiempo y para esto necesitamos distintos hilos de ejecución, de crearlos, ejecutarlos y eliminarlos se encarga este main. Además, también al inicio, se encarga de crear una pequeña ventana de configuración en la que podremos actualizar las variables globales que comentamos al principio, esto lo haremos mediante una libreria llamada 'tkinter'
```
#inicializamos las clases de variables globales
mundoConfig = MundoConfig()  
enfermedadConfig = EnfermedadConfig()  
individuoConfig = IndividuoConfig()

#ventana para configurar los parametros  
ventana = tk.Tk()  
ventana.title("Configuracion")  
ventana.geometry("1200x800")

Creamos todas las etiquetas y entradas de la ventana

def modificar()
		Modifica las variables globales con los nuevos datos cuando se pulsa el boton de 'modificar' e inicia la ejecución

ventana.mainloop()

#inicializamos las clases datos, mundo y grafica
ejecutar = true
datos = Datos(individuoConfig)  
mundo = Mundo(ejecutar, datos, mundoConfig, individuoConfig, enfermedadConfig)  
grafica = Grafica(ejecutar, datos)

# Crear hilos para generar datos y graficar en paralelo  
generator_thread = threading.Thread(target=mundo.run)  
plotter_thread = threading.Thread(target=grafica.update_plot)

# Iniciar los hilos  
generator_thread.start()  
plotter_thread.start()

#Esperar y terminar la ejecución cuando termine la espera
time.sleep(120)  
ejecutar = False  
mundo.setJugando(ejecutar)  
grafica.setEjecutando(ejecutar)  
  
# Esperar a que los hilos terminen
generator_thread.join()  
plotter_thread.join()  
  
#Imprimir los ultimos datos por consola
print(datos.getPicoInfectados())  
print(datos.getDiaPicoInfectados())  
print(datos.getMediaInfectados())

```
