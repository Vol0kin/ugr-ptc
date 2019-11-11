import numpy as np
from collections import Counter

def abs_rel_population_variance(population, col_keys, use_genders=False):
    """
    Funcion para obtener las variaciones absoultas y relativas
    de una poblacion dada
    
    Args:
        population: Poblacion de la que extraer informacion
        col_keys: Claves de las columnas
        use_genders: Indica si se debe estraer informacion de los generos
                     (defualt False)
    
    Returns:
        Diccionario con las variaciones abosultas y relativas para un
        conjunto de años para una determianda poblacion
    """
    # Obtener claves validas
    if use_genders:
        valid_keys = [k for k in col_keys if "H" in k or "M" in k]
    else:
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
        # Dependiendo de si se esta utilizando informacion sobre los generos
        # o no se hara de una u otra forma
        if use_genders:
            # Convertir los datos en una matriz (2, N), donde N es
            # el numero de años para los que se calculara la variacion
            pop = pop.reshape(2, -1)

            # Calcular variaciones
            # Se calculan para todos los años a la vez y para cada genero
            abs_variation = pop[:, :-1] - pop[:, 1:]
            rel_variation = (abs_variation / pop[:, 1:]) * 100

            # Hacer que los las variaciones sean vectores 1D
            # De esta forma se facilita procesamiento posterior
            abs_variation = abs_variation.flatten()
            rel_variation = rel_variation.flatten()
        else:
            # Calcular variaciones
            # Se calculan para todos los años a la vez
            abs_variation = pop[:-1] - pop[1:]
            rel_variation = (abs_variation / pop[1:]) * 100
        
        # Convertir a lista
        variation = abs_variation.tolist() + rel_variation.tolist()

        # Actualizar informacion
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


def get_comms_most_mean_population(population, col_keys, num_comms=10):
    """
    Funcion para obtener las num_comms comunidades con mayor poblacion media

    Args:
        population: Estructura de diccionarios que contiene la informacion
        col_keys: Claves de las columnas
        num_comms: Numero de comunidades autonomas a obtener (default 10)
    
    Returns:
        Lista con los nombres de las comunidades
    """

    # Obtener claves poblacion total
    keys_t = [k for k in col_keys if "T" in k]

    # Crear diccionario que contendra los valores medios de poblacion
    comm_mean_pop = {}

    # Obtener valores medios para cada comunidad
    for comm, pop_info in population.items():
        # Obtener valores de la poblacion para cada uno de los años
        pop = [pop_info[k] for k in keys_t]

        # Calcular valor medio de la poblacion
        pop = np.array(pop)
        pop_mean = np.mean(pop)

        # Actualizar valores
        comm_mean_pop[comm] = pop_mean
    
    # Crear Counter con el diccionario obtenido anteriormente
    counter_comm = Counter(comm_mean_pop)

    # Obtener elementos mas comunes (aquellos con mayor valor medio)
    most_pop_comm = counter_comm.most_common(num_comms)

    # Obtener lista de comunidades
    most_pop_comm_list = [comm[0] for comm in most_pop_comm]

    return most_pop_comm_list
