from utils import read_csv
import numpy as np

def get_population_variation_province(filename):
    # Obtener un diccionario con la informacion sobre la poblacion
    # a partir del fichero CSV
    population_dict = read_csv.read_csv_file(filename)

    # Crear diccionario que contendra la informacion de salida
    pop_variation_dict = {}

    # Crear lista con las claves para los tipos de variacion
    variation_keys = ["Variación absoulta", "Variación relativa"]

    for prov, pop_info in population_dict.items():
        pop_years_num = pop_info["Total"]

        years_list = [year for year in pop_years_num.keys()]
        population = np.array([pop for pop in pop_years_num.values()], dtype=np.int)

        abs_variation = population[:-1] - population[1:]
        rel_variation = (abs_variation / population[1:]) * 100

        # Crear diccionario que contiene los tipos de variacion y los
        # valores calculados
        variation_dict = {type: variation for type, variation in zip (variation_keys, [abs_variation, rel_variation])}

        # Guardar la informacion calculada para cada provincia
        pop_variation_dict[prov] = {type: {year: variation for year, variation in zip(years_list, variation_dict[type])}
                                    for type in variation_keys}

        
    print(pop_variation_dict)
    return pop_variation_dict

get_population_variation_province("datos/poblacionProvinciasHM2010-17.csv")