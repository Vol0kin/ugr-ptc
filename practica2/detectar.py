# -*- coding: utf-8 -*-

import numpy as np
from predecir import predecir
from capturar import init_entorno, capturar_guardar_imagen, stop_simulacion_conexion
import vrep
import time
import os
import sys
import glob

def rotar_robot(gamma, robot, motor_izq, motor_dcha):
    """
    Funcion para rotar al robot y los motores izquierdo y derecho gamma
    radianes.

    Args:
        gamma: Radianes en los que rotar el robot con los motores.
        robot: Handler del robot.
        motor_izq: Handler del motor izquierdo.
        motor_dcha: Handler del motor derecho
    """
    vrep.simxSetObjectOrientation(clientID, robot, -1, np.array([0.0, 0.0, gamma]), vrep.simx_opmode_oneshot)
    vrep.simxSetObjectOrientation(clientID, motor_izq, -1, np.array([0.0, 0.0, gamma]), vrep.simx_opmode_oneshot)
    vrep.simxSetObjectOrientation(clientID, motor_dcha, -1, np.array([0.0, 0.0, gamma]), vrep.simx_opmode_oneshot)

    # Esperar un segundo hasta que se complete la operacion
    time.sleep(1)


def calcular_distancias_objetos(objetos):
    """
    Funcion que calcula la distancia de un conjunto de puntos al origen de coordenadas.

    Args:
        objetos: Array con las coordenadas (x,y) de los objetos.
    
    Return:
        Devuelve un array con las ditancias.
    """
    distancias = np.linalg.norm(objetos, axis=1)

    return distancias


def calcular_orientaciones(objetos):
    # Obtener las distancias a los objetos
    distancias_objetos = calcular_distancias_objetos(objetos)

    # Obtener las distancias a los objetos cuando estan sobre el eje X
    objetos_x_axis = np.copy(objetos)
    objetos_x_axis[:,1] = 0.0
    distancias_obj_x_axis = calcular_distancias_objetos(objetos_x_axis)

    # Calcular las orientaciones
    orientaciones = np.arccos(distancias_obj_x_axis / distancias_objetos)

    # Determinar donde la orientacion tiene que ser negativa porque el objeto esta
    # a la derecha del (0,0) (valor Y negativo)
    idx_neg_orient = np.where(objetos[:,1] < 0.0)

    # Transformar valores
    orientaciones[idx_neg_orient] = np.negative(orientaciones[idx_neg_orient])

    return orientaciones
    

def escribir_comienzo_fichero(fichero):
    """
    Funcion que escribe el comienzo del fichero de resultados.

    Args:
        fichero: Fichero donde escribir.
    """
    lineas_fich = """<!DOCTYPE html>
    <html>
        <head>
            <title>Tabla predicciones</title>
            <meta charset="utf-8">
            <link rel="stylesheet" href="style/estilo.css">
        </head>
        <body>
            <h1>Tabla de predicciones y valores reales de los objetos de test</h1>
            <table>
                <tr>
                    <th>Tipo de objeto Real</th>
                    <th>Valor de la predicción</th>
                    <th>Distancia al robot</th>
                    <th>Imagen del objeto</th>
                </tr>"""

    fichero.write(lineas_fich)


def escribir_fila(fich, valor_real, valor_pred, dist, img):
    """
    Funcion que escribe una fila de la tabla en el fichero correspondiente.

    Args:
        fich: Fichero donde escribir.
        valor_real: Valor real de la clase.
        valor_pred: Valor predicho de la clase.
        img: Ruta de la imagen que insertar.
    """
    fila = f"""
                <tr>
                    <td>{valor_real}</td>
                    <td>{valor_pred}</td>
                    <td>{dist:.2f}</td>
                    <td><img src="{img}" alt="Objeto detectado"></td>
                </tr>"""
    
    fich.write(fila)


def escribir_final_fichero(fichero):
    """
    Funcion que escribe el final del fichero de resultados.

    Args:
        fichero: Fichero donde escribir.
    """
    lineas_final = """
            </table>
        </body>
    </html>
    """

    fichero.write(lineas_final)


if __name__ == "__main__":
    # Iniciar entorno de V-REP
    clientID, camara = init_entorno()

    # Predecir escena
    _, _, centroides_clusters, clases_cluster, centroides_solitarios, clases_solitarios = predecir(clientID)

    # Obtener referencia al robot
    _, robot = vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx', vrep.simx_opmode_oneshot_wait)
    _, motor_izq = vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx_leftMotor', vrep.simx_opmode_oneshot_wait)
    _, motor_dcha = vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx_rightMotor', vrep.simx_opmode_oneshot_wait)
    
    # Concatenar los centroides emparejados con los solitarios ademas de las clases
    centroides_clusters = np.concatenate([centroides_clusters, centroides_solitarios.reshape(1,-1)], axis=0)
    clases_cluster += clases_solitarios

    # Obtener las distancias de los centroides de los clusters (los objetos)
    dist_cent_cluster = calcular_distancias_objetos(centroides_clusters)

    # Obtener las orientaciones
    orientaciones = calcular_orientaciones(centroides_clusters)
    
    # Establecer valores reales
    # IMPORTANTE: LOS VALORES SON ESTATICOS, CON LO CUAL SE RECOMIENDA NO
    # MODIFICAR LA ESCENA, YA QUE NO SE CORRESPONDERAN CON LOS OBJETOS REALES
    valores_reales = ["Pierna", "No pierna", "Pierna", "Pierna"] + ["No pierna"] * 7 + ["Pierna", "No pierna"] * 2 + ["No pierna"]

    # Ordenar informacion segun el orden de las orientaciones
    idx_ord_orient = np.argsort(orientaciones)
    orientaciones = orientaciones[idx_ord_orient]
    clases_cluster = np.array(clases_cluster)
    clases_cluster = clases_cluster[idx_ord_orient]
    valores_reales = np.array(valores_reales)
    valores_reales = valores_reales[idx_ord_orient]

    # Crear directorio de salida de imagenes si no existe
    out_dir = "media"

    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
    
    # Tomar fotos y guardarlas en el directorio media/
    for i, gamma in enumerate(orientaciones):
        rotar_robot(gamma, robot, motor_izq, motor_dcha)
        capturar_guardar_imagen(clientID, camara, f"{out_dir}/objeto{i}.jpg")

    # Obtener lista con los ficheros de las imagenes
    imagenes = list(glob.glob("media/objeto*.jpg"))
    imagenes.sort(key=lambda f: int("".join(list(filter(str.isdigit, f)))))

    # Escribir resultados en fichero HTML
    with open("resultados.html", "w") as f:
        escribir_comienzo_fichero(f)

        # Escribir cada fila de la tabla
        for vr, vp, dist, img in zip(valores_reales, clases_cluster, dist_cent_cluster, imagenes):
            escribir_fila(f, vr, vp, dist, img)
        
        # Escribir final fichero
        escribir_final_fichero(f)

    # Detener simulacion
    stop_simulacion_conexion(clientID)
