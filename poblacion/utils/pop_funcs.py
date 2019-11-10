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

    # Obtener informacion de salida para cada fila
    for prov, pop_info in population.items():
        # Obtener habitantes
        pop = np.array([pop_info[k] for k in valid_keys], dtype=np.int)

        # Calcular variaciones
        abs_variation = pop[:-1] - pop[1:]
        rel_variation = (abs_variation / pop[1:]) * 100

        variation = abs_variation.tolist() + rel_variation.tolist()

        pop_variation_dict[prov] = {year: var for year, var in zip(var_keys, variation)}
    
    return pop_variation_dict


def population_community(population, col_keys, communities, provinces):
    """
    Funcion que permite calcular la poblacion total para cada categoria
    para cada una de las comunidades autonomas especificadas

    Args:
        population: Informacion sobre la poblacion de cada provincia para cada
                    categoria
        col_keys: Claves de las columnas
        communities: Lista de comunidades autonomas de las que se quiere obtener
                     informacion sobre la poblacion
        provinces: Diccionario con las provincias de cada comunidad autonoma
    
    Returns:
        Diccionario con la poblacion para cada categoria para cada una de las comunidades
        autonomas que se hayan especificado
    """
    # Crear diccionario de salida
    pop_community = {}
    

    # Generar informacion para las comunidades indicadas
    for community in communities:
        # Obtener la lista de provincias
        provinces_list = provinces[community]

        # Crear lista vacia que contendra la informacion sobre la poblacion
        # en cada una de las categorias para cada provincia
        pop_provinces = []

        # Obtener informacion de cada provincia
        for province in provinces_list:
            pop_provinces.append([population[province][k] for k in col_keys])
        
        # Convertir los datos en una matriz y sumarlos
        pop_provinces = np.array(pop_provinces, dtype=np.int)
        pop = np.sum(pop_provinces, axis=0)

        # Actualizar informacion sobre la comunidad
        pop_community[community] = {y: p for y, p in zip(col_keys, pop)}
    
    return pop_community
            