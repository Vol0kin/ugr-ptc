# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

from sklearn.svm import SVC
import pickle

# Ignorar warnings
from warnings import simplefilter

simplefilter(action='ignore', category=FutureWarning)
simplefilter(action='ignore', category=DeprecationWarning)

def visualizar_datos(dataframe):
    """
    Funcion que permite hacer un grafico en 3D con los puntos que forman el dataset.

    Args:
        dataframe: Conjunto de datos que se quiere dibujar
    """
    # Obtener las clases y establecer un color para cada una
    # Azul -> no pierna, rojo -> pierna
    clases = dataframe.clase.unique()
    colores = ["b", "r"]

    # Crear grafico 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    # Dibujar los elementos de cada clase con su color correspondiente
    for clase, color in zip(clases, colores):
        data_clase = dataframe.loc[dataframe["clase"] == clase]
        ax.scatter(data_clase.perimetro, data_clase.profundidad, data_clase.anchura, c=color)
    
    # Establecer nombres de los ejes y titulo
    ax.set_xlabel(dataframe.columns.values[0])
    ax.set_ylabel(dataframe.columns.values[1])
    ax.set_zlabel(dataframe.columns.values[2])
    plt.title("Distribucion de las clases piernas y no piernas")
    
    plt.show()



# Establecer nombres de las columnas
columnas = ["perimetro", "profundidad", "anchura", "clase"]

# Leer los datos y guardarlos en un Dataframe
df = pd.read_csv("piernasDataset.csv", names=columnas)

# Visualizacion de los datos
visualizar = False

if visualizar:
    visualizar_datos(df)

