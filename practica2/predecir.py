# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from capturar import init_entorno, procesar_ciclo, stop_simulacion_conexion
from agrupar import procesar_clusters_muestra, generar_informacion_cluster
from caracteristicas import generar_caracteristicas_clusters_muestra 
from sklearn.externals import joblib
from sklearn.neighbors import KDTree

def calcular_centroide(cluster):
    """
    Funcion que calcula el centroide de un conjunto de puntos. El centroide
    es la media de la suma de las coordenadas (x,y) de todos los puntos.

    Args:
        cluster: Conjunto de puntos de los que extraer el centroide
    
    Return:
        Devuelve el centroide.
    """
    centroide = np.mean(cluster, axis=0)

    return centroide.reshape(1,-1)


def calcular_centroides_clusters(clusters):
    """
    Funcion que calcula los centroides para un grupo de clusters

    Args:
        clusters: Clusters de los que obtener los centroides
    
    Return:
        Devuelve los centroides de cada cluster
    """
    centroides = [calcular_centroide(cluster) for cluster in clusters]

    # Juntar todos los elementos en una unica estructura
    centroides = np.concatenate(centroides, axis=0)

    return centroides


def calcular_punto_medio_centroides(centroides, clases):
    """
    Funcion que calcula el punto medio entre dos clusters cercanos de la misma
    clase. Se busca para cada centroide el centroide mas cercano (que no sea el mismo)
    y, si ambos son de la misma clase, se calcula el punto medio de la linea que une
    los dos centroides, representando la posicion del objeto.

    Args:
        centroides: Centroides de los que se quieren calcular los puntos medios.
        clases: Clase de cada centroide.
    
    Return:
        Devuelve los puntos medios para los centroides que se pueden relacionar
        correctamente, la clase a la que pertenecen, los centroides tal cual que no son
        emparejados y la clase a la que pertenecen 
    """
    puntos_medios = []
    clases_puntos_medios = []

    # Conjunto de indices de puntos que han sido emparejados
    emparejados = set()

    # Conjunto con indices ya procesados (evitar puntos repetidos)
    indx_procesado = set()

    # Crear KDTree para simplificar las busquedas
    kdtree = KDTree(centroides)

    # Escoger el segundo elemento mas cercano a cada cluster (el primero es el mismo
    # cluster)
    indx_cercano = kdtree.query(centroides, k=2, return_distance=False)[:, 1]

    for i in range(len(centroides)):
        centroide = centroides[i]

        # Obtener centroide mas cercano
        mas_cercano = indx_cercano[i]

        # Si son de la misma clase y no se ha procesado el punto actual
        # anteriormente se obtiene el punto medio y la clase
        if clases[i] == clases[mas_cercano] and i not in indx_procesado:
            punto_medio = (centroide + centroides[mas_cercano]) / 2
            puntos_medios.append(punto_medio.reshape(1,-1))
            indx_procesado.add(mas_cercano)
            clases_puntos_medios.append(clases[i])

            # Añadir los puntos a los emparejados
            emparejados.add(i)
            emparejados.add(mas_cercano)
    
    # Obtener los puntos no emparejados y la clase a la que pertenecen
    puntos_solitarios = [centroides[i] for i in range(len(centroides)) if i not in emparejados]
    clases_solitarias = [clases[i] for i in range(len(clases)) if i not in emparejados]

    
    return (np.concatenate(puntos_medios, axis=0),
            clases_puntos_medios,
            np.concatenate(puntos_solitarios, axis=0),
            clases_solitarias)


def plot_prediccion(clusters, centroides_clusters, clases):
    """
    Funcion que permite dibujar los clusters con el color asociado a la clase.
    Ademas, dibuja el punto medio de las parejas de clusters que estan cerca
    unas de otras (el centroide de la pareja de clusters de la misma clase)

    Args:
        clusters: Conjunto de clusters que representar.
        centroides_clusters: Puntos medios que unen los centroides de cada pareja
                             de clusters proximos de la misma clase.
        clases: Clases predichas.
    """
    # Obtener listas con los indices de las etiquetas positivas y negativas
    no_piernas = np.where(clases == 0)[0].tolist()
    piernas = np.where(clases == 1)[0].tolist()

    # Obtener clusters de piernas y no piernas
    clusters_no_piernas = [clusters[i] for i in no_piernas]
    clusters_piernas = [clusters[i] for i in piernas]

    # Obtener puntos que forman cada conjunto de clusters
    puntos_no_piernas = np.concatenate(clusters_no_piernas, axis=0)
    puntos_piernas = np.concatenate(clusters_piernas, axis=0)

    # Pintar clusters junto con los puntos medios
    plt.plot(puntos_no_piernas[:,0], puntos_no_piernas[:,1], "b.", label="No pierna")
    plt.plot(puntos_piernas[:,0], puntos_piernas[:,1], "r.", label="Pierna")
    plt.plot(centroides_clusters[:,0], centroides_clusters[:,1], ".", color="orange", label="Centroides")

    plt.legend()
    plt.title("Clasificacion de los objetos detectados por el sensor laser")
    plt.show()


def predecir(clientID):
    """
    Funcion que predice los clusters, los centroides de los clusters y las
    clases de cada cluster.

    Args:
        clientID: ID del cliente conectado al servidor de V-REP.
    
    Return:
        Devuelve los clusters detectados, las clases de los clusters,
        los centroides entre los clusters, las clases de dichos centroides,
        los centroides que no se pueden emparejar y las clases de dichos centroides
    """
    # Obtener la muestra
    muestra = procesar_ciclo(clientID, 0, 0)

    # Obtener cluster y generar informacion a partir de la muestra
    clusters = procesar_clusters_muestra(muestra)
    clusters_info = generar_informacion_cluster(clusters)

    # Obtener caracteristicas
    caract = generar_caracteristicas_clusters_muestra(clusters_info)

    # Cargar el clasificador
    clasificador = joblib.load("modelo.joblib")

    # Predecir
    clases = clasificador.predict(caract)

    # Obtener los centroides de los clusters
    centroides = calcular_centroides_clusters(clusters)

    # Obtener los puntos medios de las lineas que unen los centroides/clusters proximos
    centroides_clusters, clases_centroides, puntos_solitarios, clases_solitarios = calcular_punto_medio_centroides(centroides, clases)

    return clusters, clases, centroides_clusters, clases_centroides, puntos_solitarios, clases_solitarios


if __name__ == "__main__":
    # Iniciar entorno de V-REP
    clientID, camara = init_entorno()

    # Obtener los clusters, los centroides de los clusters y las clases
    clusters, clases, centroides_clusters, _, _, _ = predecir(clientID)

    # Mostrar predicción
    plot_prediccion(clusters, centroides_clusters, clases)

    # Detener simulacion
    stop_simulacion_conexion(clientID)
