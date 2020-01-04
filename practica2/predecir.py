# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from capturar import establecer_conexion, obtener_camara_handler, procesar_ciclo, stop_simulacion_conexion
from agrupar import procesar_clusters_muestra, generar_informacion_cluster
from caracteristicas import generar_caracteristicas_clusters_muestra 
from sklearn.externals import joblib
import json

def plot_prediccion(clusters, clases):

    no_piernas = np.where(clases == 0)[0].tolist()
    piernas = np.where(clases == 1)[0].tolist()

    clusters_no_piernas = [clusters[i] for i in no_piernas]
    clusters_piernas = [clusters[i] for i in piernas]

    puntos_no_piernas = np.concatenate(clusters_no_piernas, axis=0)
    puntos_piernas = np.concatenate(clusters_piernas, axis=0)

    plt.plot(puntos_no_piernas[:,0], puntos_no_piernas[:,1], "b.", label="No pierna")
    plt.plot(puntos_piernas[:,0], puntos_piernas[:,1], "r.", label="Pierna")

    plt.legend()
    plt.title("Clasificacion de los objetos detectados por el sensor laser")
    plt.show()


if __name__ == "__main__":
    # Establecer conexion
    clientID = establecer_conexion()

    # Obtener informacion de la camara
    camara = obtener_camara_handler(clientID)

    # Obtener la muestra
    muestra = procesar_ciclo(clientID, 0, 0)

    # Detener simulacion
    stop_simulacion_conexion(clientID)

    # Obtener cluster y generar informacion a partir de la muestra
    clusters = procesar_clusters_muestra(muestra)
    clusters_info = generar_informacion_cluster(clusters)

    # Obtener caracteristicas
    caract = generar_caracteristicas_clusters_muestra(clusters_info)

    # Cargar el clasificador
    clasificador = joblib.load("modelo.joblib")

    # Predecir
    clases = clasificador.predict(caract)

    plot_prediccion(clusters, clases)

    
