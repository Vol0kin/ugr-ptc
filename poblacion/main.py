from utils import pop_funcs
from utils import read_csv
from utils import graphics
from utils.html_reader import HTMLReader
from utils.html_writer import HTMLWriter

if __name__ == "__main__":
    # Obtener datos de poblacion y claves de columnas
    population, col_keys = read_csv.read_csv_file("datos/poblacionProvinciasHM2010-17.csv")

    # Crear objetos de lectura y escritura de HTML
    reader = HTMLReader()
    writer = HTMLWriter()

    ###########################################################################
    # R1
    ###########################################################################
    # Obtener variaciones
    pop_prov_variation = pop_funcs.abs_rel_population_variance(population, col_keys)

    # Crear tabla de salida
    writer.write_table(pop_prov_variation,
                       "Variación de la población de cada provincia entre 2011 y 2017",
                       "variacionProvincias.htm", variation=True)

    ###########################################################################
    # R2
    ###########################################################################
    # Leer datos de comunidades
    reader.read_html("datos/comunidadesAutonomas.htm")
    communities = reader.read_communities()

    # Leer datos de comunidades autonomas-provincias
    reader.read_html("datos/comunidadAutonoma-Provincia.htm")
    provinces = reader.read_communities_provinces()

    # Obtener datos de poblacion por provincia
    pop_community = pop_funcs.population_community(population, col_keys, communities, provinces)

    # Crear tabla de salida
    writer.write_table(pop_community,
                       "Población de cada Comunidad Autónoma entre 2010 y 2017",
                       "poblacionComAutonomas.htm", use_genders=True)
    
    ###########################################################################
    # R3
    ###########################################################################
    # Obtener comunidades con mayor poblacion media
    most_pop_comm = pop_funcs.get_comms_most_mean_population(pop_community, col_keys)

    # Crear grafico de barras
    graphics.bar_plot_man_woman(pop_community, most_pop_comm, "graficos-barra-hm.png")

    # Crear tabla de salida con grafico
    writer.write_table(pop_community,
                       "Población de cada Comunidad Autónoma entre 2010 y 2017",
                       "poblacionComAutonomas.htm", use_genders=True,
                       img_path="resultados/graficos-barra-hm.png")
    
    ###########################################################################
    # R4
    ###########################################################################
    # Obtener variacion para las comunidades para cada sexo
    comm_variation = pop_funcs.abs_rel_population_variance(pop_community, col_keys, 
                                                           use_genders=True)
    
    # Crear tabla de salida
    writer.write_table(comm_variation,
                       "Variación de la población de cada Comunidad Autónoma entre 2011 y 2017",
                       "variacionComAutonomas.htm", variation=True ,use_genders=True)
    
    ###########################################################################
    # R5
    ###########################################################################
    # Crear grafico de lineas
    graphics.plot_lines_pop_evolution(pop_community, col_keys, most_pop_comm,
                                      "graficos-lineas-t.png")
    
    # Crear tabla de salida con grafico
    writer.write_table(comm_variation,
                       "Variación de la población de cada Comunidad Autónoma entre 2011 y 2017",
                       "variacionComAutonomas.htm", variation=True ,use_genders=True,
                       img_path="resultados/graficos-lineas-t.png")