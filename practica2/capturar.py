# -*- coding: utf-8 -*-
"""
    Vrep y OpenCV en Python
    Codigo escrito por Glare
    www.robologs.net
    Modificado para practica PTC por Eugenio Aguirre
    Leemos datos de laser, los mostramos con matplot y los salvamos a un fichero JSON
    Importante: La escena tiene que estar ejecutándose en el simulador (Usar botón PLAY)
"""
import vrep
import sys
import cv2
import numpy as np
import time
import matplotlib.pyplot as plt
import json
import os
import glob
import re

# Datos de entrada
nom_fichero = input("Introduzca el nombre del fichero de salida: ")
dir_salida = input("Introduzca el directorio de salida: ")
ciclos_lectura = int(input("Introduzca el numero de ciclos de lectura: "))
segundos = int(input("Introduzca el numero de segundos entre lectura y lectura: "))

# Obtener el tipo de directorio
tipo_dir = re.findall(r"[a-zA-Z]+", dir_salida)[0]

# Eliminar .json del fichero de entrada (usado para las imagenes)
nom_fich_img = nom_fichero.replace(".json", "")

# Terminar todas las conexiones e iniciar una nueva
vrep.simxFinish(-1)
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5)

# Comprobar si se ha podido establecer la conexion
if clientID!=-1:
    print ('Conexion establecida')
else:
    sys.exit("Error: no se puede conectar. Tienes que iniciar la simulación antes de llamar a este script.")
 
# Guardar la referencia al robot y camara
_, robothandle = vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx', vrep.simx_opmode_oneshot_wait)
_, camhandle = vrep.simxGetObjectHandle(clientID, 'Vision_sensor', vrep.simx_opmode_oneshot_wait)
 
# Acceder a los datos del laser
_, datosLaserComp = vrep.simxGetStringSignal(clientID,'LaserData',vrep.simx_opmode_streaming)

#Iniciar la camara y esperar un segundo para llenar el buffer
_, resolution, image = vrep.simxGetVisionSensorImage(clientID, camhandle, 0, vrep.simx_opmode_streaming)
time.sleep(1)

# Mostrar directorio de trabajo
print("Directorio de trabajo es: ", os.getcwd())

# Ver si existe el directorio de salida y crearlo en caso de que no
dir_list = sorted(glob.glob(tipo_dir+"*"))

if dir_salida in dir_list and os.path.isdir(dir_salida):
    print("El directorio de salida ya existe")
else:
    print("El directorio de salida no existe. Creando...")
    os.mkdir(dir_salida)

# Cambiar el directorio de trabajo al de salida
os.chdir(dir_salida)
print(f"Cambiando al directorio de trabajo {os.getcwd()}")

# Crear fichero de salida y escribir cabecera
fichero_laser = open(nom_fichero, "w")

cabecera={"TiempoSleep":segundos,
          "MaxIteraciones":ciclos_lectura}

fichero_laser.write(json.dumps(cabecera)+'\n')

for iter in range(ciclos_lectura):
    # Obtener coordenadas x,y,z detectadas por laser
    puntosx=[]
    puntosy=[]
    puntosz=[]

    # Obtener señal y esperar
    returnCode, signalValue = vrep.simxGetStringSignal(clientID,'LaserData',vrep.simx_opmode_buffer)

    # Esperar para procesar los datos
    print(f"Leidos datos en iteracion {iter}. Esperando {segundos} seg. para procesarlos...")
    time.sleep(segundos)

    datosLaser=vrep.simxUnpackFloats(signalValue)

    for indice in range(0,len(datosLaser),3):
        puntosx.append(datosLaser[indice+1])
        puntosy.append(datosLaser[indice+2])
        puntosz.append(datosLaser[indice])
    
    # Guardar los puntosx, puntosy en el fichero JSON
    lectura={"Iteracion":iter, "PuntosX":puntosx, "PuntosY":puntosy}
    fichero_laser.write(json.dumps(lectura)+'\n')
    
    # Obtener frame de la camara, rotarlo y convertirlo a BGR
    _, resolution, image=vrep.simxGetVisionSensorImage(clientID, camhandle, 0, vrep.simx_opmode_buffer)
    img = np.array(image, dtype = np.uint8)
    img.resize([resolution[0], resolution[1], 3])
    img = np.rot90(img,2)
    img = np.fliplr(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Guardar imagen si es en la primera o la ultima iteracion
    if iter == 0 or iter == ciclos_lectura - 1:
        print(f"\tGuardando imagen en iteracion{iter}")
        cv2.imwrite(nom_fich_img + str(iter) + ".jpg", img)
   
time.sleep(1)

# Detener la simulacion
vrep.simxStopSimulation(clientID,vrep.simx_opmode_oneshot_wait)

# Cerrar la conexion
vrep.simxFinish(clientID)

# Escribir final del fichero
finFichero={"Iteraciones totales":ciclos_lectura}
fichero_laser.write(json.dumps(finFichero)+'\n')
fichero_laser.close()
    