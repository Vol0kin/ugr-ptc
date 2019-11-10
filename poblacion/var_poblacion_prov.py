from utils import read_csv
from utils.html_writer import HTMLWriter
import numpy as np

def abs_rel_population_variance(population, col_keys):
    """
    Funcion para obtener las variaciones absoultas y relativas
    de una poblacion dada
    
    Args:
        population: Poblacion de la que extraer informacion
        col_keys: Claves de las columnas
    
    Returns:
        Diccionario con las variaciones abosultas y relativas para un
        conjunto de años para una determianda poblacion
    """
    # Obtener claves validas
    valid_keys = [k for k in col_keys if "T" in k]

    # Generar claves de salida combinando los tipos de variacion con col_keys
    var_keys = [k + var for var in ["Abs", "Rel"] for k in valid_keys if "2010" not in k]

    # Crear diccionario que contendra la informacion de salida
    pop_variation_dict = {}

    # Crear lista con las claves para los tipos de variacion
    variation_keys = ["Variación absoulta", "Variación relativa"]

    # Obtener informacion de salida para cada fila
    for prov, pop_info in population.items():
        # Obtener habitantes
        pop = np.array([population[prov][k] for k in valid_keys], dtype=np.int)

        # Calcular variaciones
        abs_variation = pop[:-1] - pop[1:]
        rel_variation = (abs_variation / pop[1:]) * 100

        variation = abs_variation.tolist() + rel_variation.tolist()

        pop_variation_dict[prov] = {year: var for year, var in zip(var_keys, variation)}
    
    return pop_variation_dict


def population_community(population, communities, provinces):

    # Crear diccionario de salida
    pop_community = {}
    

    # Generar informacion para las comunidades indicadas
    for community in communities:
        provinces_list = provinces[community]
        # Obtener informacion de cada provincia
        for province in provinces_list:
            pop_info = population[province]
            for gender, years_pop in pop_info.items():
                pass
    