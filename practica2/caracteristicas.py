# -*- coding: utf-8 -*-

import numpy as np
import json

def calcular_perimetro(cluster):
    """
    Funcion para calcular el perimetro de un conjunto de puntos.

    Args:
        cluster: Conjunto de puntos del que obtener el perimetro
    
    Returns:
        Devuelve la suma de las distancias (perimetro).
    """
    # Obtener las distancias de cada punto al siguiente
    distancias = np.linalg.norm(cluster[1:] - cluster[:-1])

    # Sumar distnacias para obtener perimetro
    perimetro = np.sum(distancias)

    return perimetro


def calcular_anchura(cluster):
    """
    Funcion que calcula la anchura de un conjunto de puntos.
    Es decir, calcula la distancia entre el primer y el ultimo punto.

    Args:
        cluster: Conjunto de puntos de los que obtener la distancia
    
    Return:
        Devuelve la distancia entre el primer y el ultimo punto
    """
    anchura = np.linalg.norm(cluster[-1] - cluster[0])

    return anchura


def calcular_profundidad(cluster):
    """
    Funcion que calcula la profundidad de un conjunto de puntos.
    Se calcula la distancia a la recta que forman los dos extremos de los puntos
    al punto mas alejado de esta.

    Args:
        cluster: Conjunto de puntos de los que obtener la profundidad
    
    Return:
        Devuelve la distancia del punto mas alejado a la recta formada por los
        puntos que estan en los extremos
    """
    # Obtener punto inicial y final del cluster
    p1 = cluster[0]
    p2 = cluster[-1]

    # Calcular distancias de cada punto a la recta utilizando el producto vectorial
    distancias = np.array([np.linalg.norm(np.cross(p2 - p1, p - p1)) / np.linalg.norm(p2 - p1) for p in cluster[1:-1]])

    # Obtener la profundidad (la distancia maxima)
    profundidad = np.max(distancias)

    return profundidad


def calcular_caracteristicas(cluster):
    """
    Funcion que calcula las caracteristicas de un cluster de entrada

    Args:
        cluster: Conjunto de puntos del que obtener las caracteristicas
    
    Return:
        Devuelve el perimtero, la profundidad y la anchura del conjunto
        del cluster
    """
    perimetro = calcular_perimetro(cluster)
    profundidad = calcular_profundidad(cluster)
    anchura = calcular_anchura(cluster)

    return perimetro, profundidad, anchura


def generar_caracteristicas_clusters_muestra(clusters):
    """
    Funcion que genera las caracteristicas de los clusters de una muestra.

    Args:
        clusters: Lista de diccionarios que contienen la informacion de los
                  clusters.
    
    Return:
        Devuelve un array con las caracteristicas
    """
    # Crear lista de caracteristicas
    caracteristicas = []

    # Procesar cada cluster
    for cluster in clusters:
        # Obtener puntos
        puntos_x = np.array(cluster["puntosX"]).reshape(-1,1)
        puntos_y = np.array(cluster["puntosY"]).reshape(-1,1)
        puntos = np.concatenate([puntos_x, puntos_y], axis=1)

        # Obtener caracteristicas y añadirlas
        caracts = calcular_caracteristicas(puntos)

        caracteristicas.append(list(caracts))
    
    return np.array(caracteristicas)


def generar_caracteristicas_clusters(fich_clust, fich_salida, clase):
    """
    Funcion que genera las caracteristicas para un conjunto de clusters de la
    misma clase. Lee la informacion de un archivo de entrada y guarda la informacion
    en un archivo de salida, especificando la clase a la que pertenecen los
    clusters.

    Args:
        fich_clust: Fichero que contiene los clusters de los que extraer caracteristicas
        fich_salida: Fichero donde se quiere escribir la salida
        clase: Clase a la que pertenecen los clusters (0 para no pierna, 1 para pierna)
    """
    with open(fich_clust) as clusters, open(fich_salida, "w") as out:
        for cluster in clusters:
            # Cargar JSON leido
            c = json.loads(cluster)

            # Obtener puntos
            puntos_x = np.array(c["puntosX"]).reshape(-1,1)
            puntos_y = np.array(c["puntosY"]).reshape(-1,1)
            puntos = np.concatenate([puntos_x, puntos_y], axis=1)

            # Obtener caracteristicas
            per, prof, anch = calcular_caracteristicas(puntos)

            # Crear objeto de salida
            obj_carac = {
                "numero_cluster": c["numero_cluster"],
                "perimetro": per,
                "profundidad": prof,
                "anchura": anch,
                "esPierna": clase
            }

            # Escribir objeto
            out.write(json.dumps(obj_carac) + "\n")


def escribir_clase(dataset, fich_clase):
    """
    Funcion para escribir los ejemplos de una clase en el fichero dataset.
    La salida tiene el formato CSV.

    Args:
        dataset: Fichero donde se va a escribir la salida.
        fich_clase: Fichero que se quiere copiar en la salida.
    """
    # Abrir fichero y copiar cada linea
    with open(fich_clase) as clase:
        for ejemplo in clase:
            datos = json.loads(ejemplo)

            # Obtener informacion a escribir
            per = datos["perimetro"]
            prof = datos["profundidad"]
            anch = datos["anchura"]
            clase = datos["esPierna"]

            # Escribir informacion
            dataset.write(f"{per},{prof},{anch},{clase}\n")


def generar_dataset(piernas, no_piernas):
    """
    Funcion que genera un dataset a partir de los ficheros de ejemplos positivos y
    de ejemplos negativos.

    Args:
        piernas: Fichero con los ejemplos positivos.
        no_piernas: Fichero con los ejemplos negativos.
    """
    # Escribir informacion en el archivo CSV
    with open("piernasDataset.csv", "w") as dataset:
        escribir_clase(dataset, no_piernas)
        escribir_clase(dataset, piernas)

if __name__ == "__main__":
    # Nombres de los ficheros de salida
    piernas = "caracteristicasPiernas.dat"
    no_piernas = "caracteristicasNoPiernas.dat"
    # Generar caracteristicas para los clusters
    generar_caracteristicas_clusters("clustersPiernas.json", piernas, 1)
    generar_caracteristicas_clusters("clustersNoPiernas.json", no_piernas, 0)

    # Generar dataset
    generar_dataset(piernas, no_piernas)