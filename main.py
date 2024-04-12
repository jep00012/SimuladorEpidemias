import threading
import time
import tkinter as tk
from tkinter import ttk
from datos import Datos
from grafica import Grafica
from mundo import Mundo
from utilidades import MundoConfig, EnfermedadConfig, IndividuoConfig

#configuracion inicial
mundoConfig = MundoConfig()
enfermedadConfig = EnfermedadConfig()
individuoConfig = IndividuoConfig()

#ventana para configurar los parametros
ventana = tk.Tk()
ventana.title("Configuracion")
ventana.geometry("1200x800")

#etiquetas
etq_poblacion = ttk.Label(text="--CONFIGURACION DEL MUNDO--")
etq_poblacion.grid(row=0, column=0)
etq_poblacion = ttk.Label(text="Poblacion:   ")
etq_poblacion.grid(row=1, column=0)
caja_poblacion = ttk.Entry(textvariable = tk.StringVar(value=mundoConfig.POBLACION))
caja_poblacion.insert(0, mundoConfig.POBLACION)
caja_poblacion.grid(row=1, column=2)

etq_capacidadHospitalaria = ttk.Label(text="Capacidad Hospitalaria:   ")
etq_capacidadHospitalaria.grid(row=2, column=0)
caja_capacidadHospitalaria = ttk.Entry(textvariable = tk.StringVar(value=mundoConfig.CAPACIDAD_HOSPITALARIA))
caja_capacidadHospitalaria.insert(0, mundoConfig.CAPACIDAD_HOSPITALARIA)
caja_capacidadHospitalaria.grid(row=2, column=2)

etq_diaInicioHospitalizacion = ttk.Label(text="Dia Inicio Hospitalizacion:   ")
etq_diaInicioHospitalizacion.grid(row=3, column=0)
caja_diaInicioHospitalizacion = ttk.Entry(textvariable = tk.StringVar(value=mundoConfig.DIA_INICIO_HOSPITALIZACION))
caja_diaInicioHospitalizacion.insert(0, mundoConfig.DIA_INICIO_HOSPITALIZACION)
caja_diaInicioHospitalizacion.grid(row=3, column=2)

etq_minimoDeInfectadosParaHospitalizar = ttk.Label(text="Minimo de Infectados para Hospitalizar:   ")
etq_minimoDeInfectadosParaHospitalizar.grid(row=4, column=0)
caja_minimoDeInfectadosParaHospitalizar = ttk.Entry(textvariable = tk.StringVar(value=mundoConfig.MINIMO_INDIVIDUOS_INFECTADOS_PARA_HOSPITALIZAR))
caja_minimoDeInfectadosParaHospitalizar.insert(0, mundoConfig.MINIMO_INDIVIDUOS_INFECTADOS_PARA_HOSPITALIZAR)
caja_minimoDeInfectadosParaHospitalizar.grid(row=4, column=2)

etq_porcentajeUsoMediasHigienicas = ttk.Label(text="Porcentaje de Uso de Medias Higienicas:   ")
etq_porcentajeUsoMediasHigienicas.grid(row=5, column=0)
caja_porcentajeUsoMediasHigienicas = ttk.Entry(textvariable = tk.StringVar(value=mundoConfig.PORCENTAJE_USO_MEDIAS_HIGIENICAS))
caja_porcentajeUsoMediasHigienicas.insert(0, mundoConfig.PORCENTAJE_USO_MEDIAS_HIGIENICAS)
caja_porcentajeUsoMediasHigienicas.grid(row=5, column=2)

etq_eficaciaMedidasHigienicas = ttk.Label(text="Eficacia de Medidas Higienicas:   ")
etq_eficaciaMedidasHigienicas.grid(row=6, column=0)
caja_eficaciaMedidasHigienicas = ttk.Entry(textvariable = tk.StringVar(value=mundoConfig.EFICACIA_MEDIDAS_HIGIENICAS))
caja_eficaciaMedidasHigienicas.insert(0, mundoConfig.EFICACIA_MEDIDAS_HIGIENICAS)
caja_eficaciaMedidasHigienicas.grid(row=6, column=2)

etq_porcentajeVacunados = ttk.Label(text="Porcentaje de Vacunados:   ")
etq_porcentajeVacunados.grid(row=7, column=0)
caja_porcentajeVacunados = ttk.Entry(textvariable = tk.StringVar(value=mundoConfig.PORCENTAJE_VACUNADOS))
caja_porcentajeVacunados.insert(0, mundoConfig.PORCENTAJE_VACUNADOS)
caja_porcentajeVacunados.grid(row=7, column=2)

etq_enfermedad = ttk.Label(text="--CONFIGURACION DE LA ENFERMEDAD--")
etq_enfermedad.grid(row=8, column=0)

etq_diasRecuperacion = ttk.Label(text="Dias de Recuperacion:   ")
etq_diasRecuperacion.grid(row=9, column=0)
caja_diasRecuperacion = ttk.Entry(textvariable = tk.StringVar(value=enfermedadConfig.DIAS_RECUPERACION[0]))
caja_diasRecuperacion.insert(0, enfermedadConfig.DIAS_RECUPERACION[0])
caja_diasRecuperacion.grid(row=9, column=2)
caja_diasRecuperacion2 = ttk.Entry(textvariable = tk.StringVar(value=enfermedadConfig.DIAS_RECUPERACION[1]))
caja_diasRecuperacion2.insert(0, enfermedadConfig.DIAS_RECUPERACION[1])
caja_diasRecuperacion2.grid(row=9, column=3)

etq_tasaMortalidad = ttk.Label(text="Tasa de Mortalidad:   ")
etq_tasaMortalidad.grid(row=10, column=0)
caja_tasaMortalidad = ttk.Entry(textvariable = tk.StringVar(value=enfermedadConfig.TASA_MORTALIDAD))
caja_tasaMortalidad.insert(0, enfermedadConfig.TASA_MORTALIDAD)
caja_tasaMortalidad.grid(row=10, column=2)

etq_tasaContagio = ttk.Label(text="Tasa de Contagio:   ")
etq_tasaContagio.grid(row=11, column=0)
caja_tasaContagio = ttk.Entry(textvariable = tk.StringVar(value=enfermedadConfig.TASA_CONTAGIO))
caja_tasaContagio.insert(0, enfermedadConfig.TASA_CONTAGIO)
caja_tasaContagio.grid(row=11, column=2)

etq_diasDetectarEnfermedad = ttk.Label(text="Dias para Detectar Enfermedad:   ")
etq_diasDetectarEnfermedad.grid(row=12, column=0)
caja_diasDetectarEnfermedad = ttk.Entry(textvariable = tk.StringVar(value=enfermedadConfig.DIAS_DETECTAR_ENFERMEDAD))
caja_diasDetectarEnfermedad.insert(0, enfermedadConfig.DIAS_DETECTAR_ENFERMEDAD)
caja_diasDetectarEnfermedad.grid(row=12, column=2)

etq_diasInmunidad = ttk.Label(text="Dias de Inmunidad:   ")
etq_diasInmunidad.grid(row=13, column=0)
caja_diasInmunidad = ttk.Entry(textvariable = tk.StringVar(value=enfermedadConfig.DIAS_INMUNIDAD[0]))
caja_diasInmunidad.insert(0, enfermedadConfig.DIAS_INMUNIDAD[0])
caja_diasInmunidad.grid(row=13, column=2)
caja_diasInmunidad2 = ttk.Entry(textvariable = tk.StringVar(value=enfermedadConfig.DIAS_INMUNIDAD[1]))
caja_diasInmunidad2.insert(0, enfermedadConfig.DIAS_INMUNIDAD[1])
caja_diasInmunidad2.grid(row=13, column=3)

#funcion para modificar los parametros de configuracion
def modificar():
    mundoConfig.POBLACION = int(caja_poblacion.get())
    mundoConfig.CAPACIDAD_HOSPITALARIA = int(caja_capacidadHospitalaria.get())
    mundoConfig.DIA_INICIO_HOSPITALIZACION = int(caja_diaInicioHospitalizacion.get())
    mundoConfig.MINIMO_INDIVIDUOS_INFECTADOS_PARA_HOSPITALIZAR = int(caja_minimoDeInfectadosParaHospitalizar.get())
    mundoConfig.PORCENTAJE_USO_MEDIAS_HIGIENICAS = float(caja_porcentajeUsoMediasHigienicas.get())
    mundoConfig.EFICACIA_MEDIDAS_HIGIENICAS = float(caja_eficaciaMedidasHigienicas.get())
    mundoConfig.PORCENTAJE_VACUNADOS = float(caja_porcentajeVacunados.get())
    enfermedadConfig.DIAS_RECUPERACION[0] = eval(caja_diasRecuperacion.get())
    enfermedadConfig.DIAS_RECUPERACION[1] = eval(caja_diasRecuperacion2.get())
    enfermedadConfig.TASA_MORTALIDAD = float(caja_tasaMortalidad.get())
    enfermedadConfig.TASA_CONTAGIO = float(caja_tasaContagio.get())
    enfermedadConfig.DIAS_DETECTAR_ENFERMEDAD = int(caja_diasDetectarEnfermedad.get())
    enfermedadConfig.DIAS_INMUNIDAD[0] = eval(caja_diasInmunidad.get())
    enfermedadConfig.DIAS_INMUNIDAD[1] = eval(caja_diasInmunidad2.get())
    ventana.destroy()

#boton para modificar los parametros de configuracion e iniciar la simulacion
boton = ttk.Button(text="Modificar", command=modificar)
boton.grid(row=14, column=0)

ventana.mainloop()

# Crear objetos
ejecutar = True
datos = Datos(individuoConfig)
mundo = Mundo(ejecutar, datos, mundoConfig, individuoConfig, enfermedadConfig)
grafica = Grafica(ejecutar, datos)

# Crear hilos para generar datos y graficar en paralelo
generator_thread = threading.Thread(target=mundo.run)
plotter_thread = threading.Thread(target=grafica.update_plot)

# Iniciar los hilos
generator_thread.start()
plotter_thread.start()

time.sleep(120)
ejecutar = False
mundo.setJugando(ejecutar)
grafica.setEjecutando(ejecutar)

# Esperar a que los hilos terminen (esto nunca sucede en este ejemplo)
generator_thread.join()
plotter_thread.join()


print(datos.getPicoInfectados())
print(datos.getDiaPicoInfectados())
print(datos.getMediaInfectados())