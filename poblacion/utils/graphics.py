import numpy as np
import matplotlib.pyplot as plt
from . import dir_check

def bar_plot_man_woman(population, most_pop_communities, outfile):
    """
    Funcion que crea un grafico de barras horizontal para las comunidades
    autonomas con una mayor poblacion durante 2017, mostrando informacion
    de la cantidad de hombres y mujeres

    Args:
        population: Estructura de donde extraer informacion sobre el numero de
                    habitantes
        most_pop_communities: Comunidades con una mayor poblacion
        outfile: Archivo de salida
    """
    # Establecer eje Y (donde se pintaran las comunidades)
    y_axis = np.arange(len(most_pop_communities))

    # Establecer ancho de las lineas
    width = 0.35

    # Establecer directorio de salida
    outdir = "resultados/"

    # Obtener datos para hombres y mujeres
    men_data = [population[comm]["H2017"] for comm in most_pop_communities]
    women_data = [population[comm]["M2017"] for comm in most_pop_communities]

    # Dibujar graficos mediante subplots
    _, ax = plt.subplots()    

    # Dibujar graficos de barras horizontales
    # Los graficos verticales no cabian
    ax.barh(y_axis, men_data, width, label="Hombres")
    ax.barh(y_axis + width, women_data, width, label="Mujeres")

    # Poner etiquetas a los ejes y titulo
    plt.xlabel("Número de personas")
    plt.ylabel("Comunidades Autónomas")
    plt.title("10 CC.AA. más pobladas en 2017")

    # Establecer ticks e invertir eje Y para que sea el principal (donde estaran
    # los nombres de las comunidades)
    # Para poner los ticks, por defecto se ponen en el primer grafico de barras
    # Si se le suma solo la anchura, se pondran en el segundo grafico de barras
    # Hay que ponerlo en el punto medio (por eso se divide la anchura entre 2)
    ax.set_yticks(y_axis + width / 2)
    ax.set_yticklabels(most_pop_communities)
    ax.invert_yaxis()

    # Establecer rotacion de los datos en el eje X
    plt.xticks(rotation=22.5)

    # Poner leyenda
    ax.legend()

    # Hacer que se el grafico sea mas compacto
    plt.tight_layout()

    # Guardar figura
    plt.savefig(f"{outdir}/{outfile}")
