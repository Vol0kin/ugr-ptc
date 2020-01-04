# -*- coding: utf-8 -*-

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

def establecer_conexion():
    """
    Funcion para establecer una conexion con el servidor de V-REP.
    Cierra todas las conexiones existentes y crea una nueva, comprobando
    si se puede establecer o no dicha conexion.

    Returns:
        Devuelve el ID del cliente si la conexion ha tenido exito.
    """
    # Terminar todas las conexiones e iniciar una nueva
    vrep.simxFinish(-1)
    clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5)

    # Comprobar si se ha podido establecer la conexion
    if clientID!=-1:
        print ('Conexion establecida')
    else:
        sys.exit("Error: no se puede conectar. Tienes que iniciar la simulación antes de llamar a este script.")
    
    return clientID


def obtener_camara_handler(clientID):
    """
    Funcion que obtiene un handler de la camara, el cual se puede utilizar
    para acceder al laser mas adelante. Ademas, inicializa el visor de la
    camara y del laser

    Args:
        clientID: ID del cliente que ha establecido una conexion con el
                  servidor de V-REP.
    Return:
        Devuelve el handler de la camara
    """
    # Obtener handler
    _, camhandle = vrep.simxGetObjectHandle(clientID, 'Vision_sensor', vrep.simx_opmode_oneshot_wait)

    # Inicializar camara y laser
    vrep.simxGetVisionSensorImage(clientID, camhandle, 0, vrep.simx_opmode_streaming)
    vrep.simxGetStringSignal(clientID, 'LaserData', vrep.simx_opmode_streaming)

    # Esperar 1 segundo hasta que se rellene el buffer
    time.sleep(1)

    return camhandle


def procesar_ciclo(clientID, segundos, iter):
    """
    Funcion que procesa un ciclo de simulacion. Obtiene los datos y los transforma
    al formato JSON especificado.

    Args:
        clientID: ID del cliente que ha establecido una conexion con el
                  servidor de V-REP.
        segundos: Numero de segundos que esperar para procesar los datos.
        iter: Numero de iteracion.
    
    Return:
        Devuelve un objeto en formato JSON especificando la iteracion y los
        puntos detectados en el eje X y en el eje Y
    """
    # Obtener coordenadas x,y,z detectadas por laser
    puntosx=[]
    puntosy=[]
    puntosz=[]

    # Obtener señal
    _, signalValue = vrep.simxGetStringSignal(clientID,'LaserData',vrep.simx_opmode_buffer)

    # Esperar para procesar los datos
    print(f"Leidos datos en iteracion {iter}. Esperando {segundos} seg. para procesarlos...")
    time.sleep(segundos)

    # Procesar datos
    datosLaser=vrep.simxUnpackFloats(signalValue)

    for indice in range(0,len(datosLaser),3):
        puntosz.append(datosLaser[indice])
        puntosx.append(datosLaser[indice+1])
        puntosy.append(datosLaser[indice+2])
        
    # Obtener lectura
    lectura = {"Iteracion":iter, "PuntosX":puntosx, "PuntosY":puntosy}

    return lectura


def stop_simulacion_conexion(clientID):
    """
    Funcion que detiene la simulacion y la conexion con el servidor de V-REP
    utilizando el ID especificado.

    Args:
        clientID: ID del cliente que ha establecido una conexion con el
                  servidor de V-REP.
    """
    # Detener la simulacion
    vrep.simxStopSimulation(clientID,vrep.simx_opmode_oneshot_wait)

    # Cerrar la conexion
    vrep.simxFinish(clientID)


if __name__ == "__main__":
    # Datos de entrada
    nom_fichero = input("Introduzca el nombre del fichero JSON de salida: ")
    dir_salida = input("Introduzca el directorio de salida: ")
    ciclos_lectura = int(input("Introduzca el numero de ciclos de lectura: "))
    segundos = int(input("Introduzca el numero de segundos entre lectura y lectura: "))

    # Obtener el tipo de directorio
    tipo_dir = re.findall(r"[a-zA-Z]+", dir_salida)[0]

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

    # Eliminar .json del fichero de entrada (usado para las imagenes)
    nom_fich_img = nom_fichero.replace(".json", "")

    # Establecer conexion con el servidor de V-REP
    clientID = establecer_conexion()

    # Obtener camara
    camhandle = obtener_camara_handler(clientID)

    # Crear fichero de salida y escribir cabecera
    fichero_laser = open(nom_fichero, "w")
    cabecera={"TiempoSleep":segundos, "MaxIteraciones":ciclos_lectura}
    fichero_laser.write(json.dumps(cabecera)+'\n')

    # Ciclo de lectura/escritura
    for iter in range(ciclos_lectura):
        # Obtener lectura y guardarla
        lectura = procesar_ciclo(clientID, segundos, iter)
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
            print(f"\tGuardando imagen en iteracion {iter}")
            cv2.imwrite(nom_fich_img + str(iter) + ".jpg", img)
    
    time.sleep(1)

    # Detener simulacion y conexion con el servidor
    stop_simulacion_conexion(clientID)

    # Escribir final del fichero
    finFichero={"Iteraciones totales":ciclos_lectura}
    fichero_laser.write(json.dumps(finFichero)+'\n')
    fichero_laser.close()
  