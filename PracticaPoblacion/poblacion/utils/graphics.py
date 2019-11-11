import numpy as np
import matplotlib.pyplot as plt
from . import dir_check

def _save_fig(outfile):
    """
    Funcion para guardar una figura. Comprueba si el directorio
    de salida existe antes de guardarla

    Args:
        outfile: Nombre de la figura a guardar
    """
    # Establecer directorio de salida
    outdir = "resultados/"

    # Comprobar que existe directorio de salida
    dir_check.check_exists_dir(outdir)

    # Guardar figura
    plt.savefig(f"{outdir}{outfile}")


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

    # Obtener datos para hombres y mujeres
    men_data = [population[comm]["H2017"] for comm in most_pop_communities]
    women_data = [population[comm]["M2017"] for comm in most_pop_communities]

    # Limpiar figura (en caso de que se haya dibujado algo antes)
    plt.clf()

    # Dibujar graficos mediante subplots
    _, ax = plt.subplots()    

    # Dibujar graficos de barras horizontales
    # Los graficos verticales no cabian
    ax.barh(y_axis, men_data, width, label="Hombres")
    ax.barh(y_axis + width, women_data, width, label="Mujeres")

    # Establecer ticks e invertir eje Y (asi los mas probables estaran arriba)
    # Para poner los ticks, por defecto se ponen en el primer grafico de barras
    # Si se le suma solo la anchura, se pondran en el segundo grafico de barras
    # Hay que ponerlo en el punto medio (por eso se divide la anchura entre 2)
    ax.set_yticks(y_axis + width / 2)
    ax.set_yticklabels(most_pop_communities)
    ax.invert_yaxis()

    # Establecer rotacion de los datos en el eje X
    plt.xticks(rotation=22.5)

    # Poner etiquetas a los ejes, titulo y leyenda
    plt.xlabel("Número de personas")
    plt.ylabel("Comunidades Autónomas")
    plt.title("10 CC.AA. más pobladas en 2017")
    ax.legend()

    # Hacer que se el grafico sea mas compacto
    plt.tight_layout()

    # Guardar figura
    _save_fig(outfile)


def plot_lines_pop_evolution(population, col_keys, most_pop_communities, outfile):
    """
    Funcion para dibujar un grafico de lineas mostrando la evolucion de la poblacion
    total para las N comunidades autonomas mas pobladas

    Args:
        population: Estructura de donde extraer informacion sobre el numero de
                    habitantes
        col_keys: Claves de las columnas
        most_pop_communities: Comunidades con una mayor poblacion
        outfile: Archivo de salida
    """
    # Obtener claves de los años
    year_keys = [k for k in col_keys if "T" in k]

    # Invertir las claves para que los años mas antiguos esten
    # al principio (orden creciente)
    year_keys.reverse()

    # Obtener los años a partir de las claves
    # Se ignora el primer caracter porque es una T
    years = [y[1:] for y in year_keys]

    # Limpiar figura (en caso de que se haya dibujado algo antes)
    plt.clf()

    # Dibujar una linea para cada comunidad
    for comm in most_pop_communities:
        # Obtener valores de la poblacion y pintarlos
        pop_values = [population[comm][y] for y in year_keys]
        plt.plot(years, pop_values, label=comm)
    
    # Establecer rotacion de los datos en el eje X
    plt.xticks(rotation=22.5)
    
    # Poner etiquetas para cada eje, titulo y leyenda
    # La leyenda se tiene que ajustar
    plt.xlabel("Años")
    plt.ylabel("Número de habitantes totales")
    plt.title("Evolución población 10 CC.AA. más pobladas")
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    # Hacer que se el grafico sea mas compacto
    plt.tight_layout()

    # Guardar figura
    _save_fig(outfile)
