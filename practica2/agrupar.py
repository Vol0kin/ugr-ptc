# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import json
import glob
import sys

MIN_PUNTOS = 3
MAX_PUNTOS = 13
UMBRAL = 0.05

def obtener_cluster_datos(puntos):
    """
    Funcion que extraer un cluster a partir de un conjunto de puntos. Se mira que
    el tamaño del cluster no supere el maximo permitido.

    Args:
        puntos: Array con los puntos de los que extraer un cluster.
    
    Return:
        Devuelve un array con los puntos que forman un cluster.
    """
    # Añadir punto inicial al cluster
    cluster = [puntos[0]]

    i = 0
    superado_umbral = False

    while not superado_umbral and len(cluster) < MAX_PUNTOS and i < len(puntos) - 1:
        # Obtener distancia entre punto actual y el siguiente
        dist = np.linalg.norm(puntos[i+1] - puntos[i])

        # Si no se supera el umbral, añadir punto al cluster
        if dist <= UMBRAL:
            cluster.append(puntos[i+1])
        else:
            superado_umbral = True
        
        # Pasar al siguiente punto
        i += 1

    return np.array(cluster)


def procesar_clusters_muestra(muestra):
    """
    Funcion que procesa una muestra de puntos y obtiene una serie de clusters
    a partir de los puntos.

    Args:
        muestra: Objeto en formato JSON que representa una muestra. El objeto
                 tiene que estar deserializado.
    
    Return:
        Devuelve los clusters que se pueden obtener en la muestra
    """
    # Lista que contendra los clusters de la muestra
    clusters_muestra = []
    
    # Obtener puntos y concatenarlos 
    # Se forma una matriz de parejas [x,y]
    puntos_x = np.array(muestra["PuntosX"]).reshape(-1,1)
    puntos_y = np.array(muestra["PuntosY"]).reshape(-1,1)
    puntos = np.concatenate([puntos_x, puntos_y], axis=1)

    # Indice para recorrer los puntos
    i = 0

    while i < len(puntos):
        # Obtener cluster
        cluster = obtener_cluster_datos(puntos[i:])

        # Si hay un minimo de puntos, añadir cluster al conjunto
        if len(cluster) >= MIN_PUNTOS:
            clusters_muestra.append(cluster)
        
        # Incrementar indice en la longitud del cluster obtenido, de forma que
        # no se procesen dos veces los mismos puntos
        i += len(cluster)

    return clusters_muestra


def procesar_clusters_fichero(fichero):
    """
    Funcion que procesa un fichero de un directorio y obtiene los clusters
    que se puedan encontrar.

    Args:
        fichero: Fichero a procesar.
    
    Return:
        Lista con los clusters que se pueden encontrar en el fichero
    """
    # Establecer clusters del fichero iniciales
    clusters_fich = []

    # Leer fichero, obtener clusters por cada muestra y añadirlos a los existentes
    with open(fichero, "r") as f:
        for muestra in f.readlines()[1:-1]:
            # Deserializar muestra antes de procesarla
            clusters_fich += procesar_clusters_muestra(json.loads(muestra))
    
    return clusters_fich


def procesar_clusters_directorios(lista_dirs):
    """
    Funcion que obtiene los clusters que se pueden encontrar en directorios
    del mismo tipo (directorios con datos positivos o con datos negativos).

    Args:
        lista_dirs: Lista con los nombres de los directorios a procesar.
    Return:
        Devuelve una lista con los clusters que se pueden obtener del conjunto
        de directorios.
    """
    # Establecer clusters inciales
    clusters = []

    # Procesar cada directorio
    for directorio in lista_dirs:
        # Obtener fichero JSON y gestionar error en caso de no encontrarse
        try:
            fichero = list(glob.glob(f"{directorio}/*.json"))[0]
        except IndexError:
            sys.exit(f"ERROR: No se ha encontrado un archivo JSON en {directorio}")
        
        # Obtener clusters del fichero y añadirlos a los existentes
        clusters_fichero = procesar_clusters_fichero(fichero)
        clusters += clusters_fichero        
    
    return clusters


def generar_informacion_cluster(clusters):
    """
    Funcion que genera la informacion necesaria de un grupo de clusters para que
    pueda ser escrita a disco posteriormente. Se genera una lista que contiene
    objetos en formato JSON.

    Args:
        clusters: Clusters de los que extraer la informacion
    
    Return:
        Devuelve una lista con los objetos que contienen la informacion necesaria
        para poder ser escritos a disco.
    """
    info_clusters = [
        {
            "numero_cluster": i,
            "numero_puntos": len(cluster),
            "puntosX": cluster[:,0].tolist(),
            "puntosY": cluster[:,1].tolist()
        }
        for i, cluster in enumerate(clusters)
    ]

    return info_clusters


def guardar_clusters(clusters, nom_archivo):
    """
    Funcion que permite guardar un conjunto de clusters a disco.

    Args:
        clusters: Conjunto de clusters a guardar.
        nom_archivo: Nombre del archivo de salida.
    """
    # Escribir informacion
    with open(nom_archivo, "w") as f:
        info_clusters = generar_informacion_cluster(clusters)

        for cluster in info_clusters:
            f.write(json.dumps(cluster) + "\n")


if __name__ == "__main__":
    print(f"Numero minimo de puntos por cluster: {MIN_PUNTOS}")
    print(f"Numero maximo de puntos por cluster: {MAX_PUNTOS}")
    print(f"Umbral (distancia max. entre puntos): {UMBRAL}")
    
    # Obtener listas compuestas por los nombres de los directorios positivos
    # y negativos
    dirs_positivo = sorted(list(glob.glob("positivo*")))
    dirs_negativo = sorted(list(glob.glob("negativo*")))

    if len(dirs_positivo) == 0 or len(dirs_negativo) == 0:
        sys.exit("Faltan directorios con muestras positivas/negativas")
    
    # Obtener los clusters asociados a cada conjunto de directorios
    clusters_pos = procesar_clusters_directorios(dirs_positivo)
    clusters_neg = procesar_clusters_directorios(dirs_negativo)

    print(f"Numero de clusters obtenidos para piernas: {len(clusters_pos)}")
    print(f"Numero de clusters obtenidos para no piernas: {len(clusters_neg)}")

    # Guardar informacion
    guardar_clusters(clusters_pos, "clustersPiernas.json")
    guardar_clusters(clusters_neg, "clustersNoPiernas.json")
