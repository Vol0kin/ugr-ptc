# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.base import clone
from sklearn.externals import joblib
import pickle

# Ignorar warnings
from warnings import simplefilter

simplefilter(action='ignore', category=FutureWarning)
simplefilter(action='ignore', category=DeprecationWarning)

SEED = 1

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


def evaluar_modelo(X, y, modelo, cv):
    """
    Funcion que evalua un modelo mediante validacion cruzada y obtiene los resultados
    medios.

    Args:
        X: Caracteristicas para entrenar el modelo.
        y: Etiquetas para entrenar el modelo.
        modelo: Modelo a entrenar.
        cv: Objeto de validacion cruzada.
    
    Return:
        Devuelve la media de la accuracy.
    """
    scores = cross_val_score(modelo, X, y, scoring='accuracy', cv=cv, n_jobs=4)

    return np.mean(scores)


def imprimir_informe(accuracy, y_val, y_pred):
    """
    Funcion que imprime por pantalla el informe de los resultados obtenidos
    al entrenar el clasificador y utilizar el conjunto de validacion para
    ver como se comporta.
    """
    print(f"Acc_val: (TP+TN)/(T+P)  {accuracy:0.4f}")

    print("Matriz de confusión Filas: verdad Columnas: predicción")
    print(confusion_matrix(y_val, y_pred))

    print("Precision= TP / (TP + FP), Recall= TP / (TP + FN)")
    print("f1-score es la media entre precisión y recall")
    print(classification_report(y_val, y_pred))


def mostrar_informe_validacion(X_train, y_train, X_val, y_val, modelo):
    # Clonar modelo (asi no es entrenado el modelo directamente)
    modelo_clon = clone(modelo)

    # Entrenar modelo clonado
    modelo_clon.fit(X_train, y_train)

    # Predecir valores
    y_pred = modelo_clon.predict(X_val)
    acc_val = accuracy_score(y_val, y_pred)

    # Mostrar resultados
    imprimir_informe(acc_val, y_val, y_pred)


# Establecer nombres de las columnas
columnas = ["perimetro", "profundidad", "anchura", "clase"]

# Leer los datos y guardarlos en un Dataframe
df = pd.read_csv("piernasDataset.csv", names=columnas)

# Visualizacion de los datos
visualizar = False

if visualizar:
    visualizar_datos(df)

# Separar datos en caracteristicas y etiquetas
X = df.drop(columns=["clase"])
y = df["clase"]

# Separar datos en conjuntos de entrenamiento y de validacion
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=SEED)

# Crear un objeto para hacer validacion cruzada
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)

# Establecer los modelos que se van a probar
modelos = {
    "SVM Kernel Lineal": SVC(kernel="linear", random_state=SEED),
    "SVM Kernel Polinomico Grad=2": SVC(kernel="poly", degree=2, random_state=SEED),
    "SVM Kernel Polinomico Grad=3": SVC(kernel="poly", degree=3, random_state=SEED),
    "SVM Kernel Polinomico Grad=4": SVC(kernel="poly", degree=4, random_state=SEED),
    "SVM Kernel RBF": SVC(kernel="rbf", random_state=SEED)
}


print("-------------------- Validacion de los modelos --------------------")
for nombre, modelo in modelos.items():
    score_medio = evaluar_modelo(X_train, y_train, modelo, cv)
    print(f"Modelo evaluado: {nombre} Accuracy media en 5-fold CV: {score_medio:0.4f}")

print("\n-------------------- Resultados de entrenamiento de los modelos --------------------")
for nombre, modelo in modelos.items():
    print(f"--------------- {nombre} ---------------")
    mostrar_informe_validacion(X_train, y_train, X_val, y_val, modelo)

# Ajustar los hiperparametros del mejor modelo
# El mejor modelo es un SVM con kernel RBF
mejor_modelo = modelos["SVM Kernel RBF"]

# Establecer grid de hiperparametros a mejorar
hyperparam_modelo = {
    "C": [0.01, 0.1, 1, 2, 3, 4, 5, 10, 50, 100]
}

# Establecer parametros del grid
grid_params = {
    "param_grid": hyperparam_modelo,
    "cv": cv,
    "n_jobs": -1,
    "scoring": "accuracy"
}

mejor_svm = GridSearchCV(mejor_modelo, **grid_params)
mejor_svm.fit(X_train, y_train)

print("\n-------------------- Mejor estimador --------------------")
print(mejor_svm.best_estimator_)

# Predecir valores
y_pred = mejor_svm.predict(X_val)
acc_val = accuracy_score(y_val, y_pred)

# Mostrar resultados
print("\n-------------------- Resultados finales --------------------")
imprimir_informe(acc_val, y_val, y_pred)

# Entrenar modelo final con todos los datos
modelo_final = SVC(kernel="rbf", random_state=SEED, **mejor_svm.best_params_)
modelo_final.fit(X, y)

# Guardar modelo para usos futuros
joblib.dump(modelo_final, "modelo.joblib")
