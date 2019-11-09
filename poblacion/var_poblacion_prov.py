from utils import read_csv
from utils.html_writer import HTMLWorker
import numpy as np

def population_variation_province(filename):
    """
    Obtener un diccionario con la informacion sobre la poblacion
    a partir del fichero CSV
    """
    population_dict = read_csv.read_csv_file(filename)

    # Crear diccionario que contendra la informacion de salida
    pop_variation_dict = {}

    # Crear lista con las claves para los tipos de variacion
    variation_keys = ["Variación absoulta", "Variación relativa"]

    # Procesar informacion
    for prov, pop_info in population_dict.items():
        # Obtener informacion sobre la poblacion total
        years_pop = pop_info["Total"]

        """
        Obtener los años y los años de salida (todos menos el primer año,
        el de valor mas bajo)
        """
        years_list = [year for year in years_pop.keys()]
        output_years = years_list[:-1]

        # Obtener poblacion de cada año
        population = np.array([pop for pop in years_pop.values()], dtype=np.int)

        # Calcular variaciones
        abs_variation = population[:-1] - population[1:]
        rel_variation = (abs_variation / population[1:]) * 100

        """
        Crear diccionario que contiene los valores calculados para cada
        tipo de variacion
        """
        variation_dict = {type: variation for type, variation in zip (variation_keys, [abs_variation, rel_variation])}

        # Guardar la informacion calculada para cada provincia
        pop_variation_dict[prov] = {type: {year: variation for year, variation in zip(output_years, variation_dict[type])}
                                    for type in variation_keys}
    
    # Escribir salida en fichero HTML
    writer = HTMLWorker("Variación población provincias 2011-2017")
    writer.write_population_var_province_years(pop_variation_dict, variation_keys, output_years,
                                               "variacionProvincias2011-17.htm")
    return pop_variation_dict