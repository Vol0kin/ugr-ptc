from utils import pop_funcs
from utils import read_csv
from utils import graphics
from utils.html_reader import HTMLReader
from utils.html_writer import HTMLWriter

if __name__ == "__main__":
    # Obtener datos de poblacion y claves de columnas
    population_prov, col_keys = read_csv.read_csv_file("datos/poblacionProvinciasHM2010-17.csv")

    # Crear objetos de lectura y escritura de HTML
    reader = HTMLReader()
    writer = HTMLWriter()

    ###########################################################################
    # R1
    ###########################################################################
    # Obtener variaciones
    pop_prov_variation = pop_funcs.abs_rel_population_variance(population_prov, col_keys)

    # Crear tabla de salida
    writer.write_table(pop_prov_variation,
                       "Variación de la población de cada provincia entre 2011 y 2017",
                       "variacionProvincias.htm", variation=True)

    ###########################################################################
    # R2
    ###########################################################################
    # Leer datos de comunidades
    communities = reader.read_communities("datos/comunidadesAutonomas.htm")

    # Leer datos de comunidades autonomas-provincias
    provinces = reader.read_communities_provinces("datos/comunidadAutonoma-Provincia.htm")

    # Obtener datos de poblacion por provincia para las comunidades
    pop_community = pop_funcs.population_community(population_prov, col_keys,
                                                   communities, provinces)

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
    
    ###########################################################################
    # R6
    ###########################################################################
    # Obtener valores de la tabla original
    orig_var_values = reader.read_table_provinces_var("datos/variacionProvincias2011-17.htm")

    # Obtener valores de la tabla resultado
    result_var_values = reader.read_table_provinces_var("resultados/variacionProvincias.htm")

    # Comparar ambos valores
    are_equal_strict = pop_funcs.compare_variation_values(orig_var_values, result_var_values,
                                                          strict_equal=True)
    are_close = pop_funcs.compare_variation_values(orig_var_values, result_var_values)

    # Mostrar salida por pantalla
    print("R6")
    print("¿Las dos tablas tienen valores estrictamente iguales? ", are_equal_strict)
    print("¿Las dos tablas tienen valores muy cercanos (margen de error 0.01)? ", are_close)

    ###########################################################################
    # Obtener tablas para comunidades BIS
    ###########################################################################
    # Leer datos de comunidades BIS
    bis_communities = reader.read_communities("datos/comunidadesAutonomasBis.htm")

    # Obtener datos de poblacion por provincia para las comunidades bis
    pop_community_bis = pop_funcs.population_community(population_prov, col_keys,
                                                       bis_communities, provinces)
    
    # Obtener comunidades BIS con mayor poblacion media
    most_pop_comm_bis = pop_funcs.get_comms_most_mean_population(pop_community_bis, col_keys)

    # Crear grafico de barras
    graphics.bar_plot_man_woman(pop_community_bis, most_pop_comm_bis, "graficos-barra-hm-bis.png")

    # Crear tabla de salida con grafico
    writer.write_table(pop_community_bis,
                       "Población de cada Comunidad Autónoma BIS entre 2010 y 2017",
                       "poblacionComAutonomasBis.htm", use_genders=True,
                       img_path="resultados/graficos-barra-hm-bis.png")
    
    # Obtener variacion para las comunidades para cada sexo
    comm_variation_bis = pop_funcs.abs_rel_population_variance(pop_community_bis, col_keys, 
                                                           use_genders=True)
    
    # Crear grafico de lineas
    graphics.plot_lines_pop_evolution(pop_community_bis, col_keys, most_pop_comm_bis,
                                      "graficos-lineas-t-bis.png")
    
    # Crear tabla de salida con grafico
    writer.write_table(comm_variation_bis,
                       "Variación de la población de cada Comunidad Autónoma entre 2011 y 2017",
                       "variacionComAutonomasBis.htm", variation=True ,use_genders=True,
                       img_path="resultados/graficos-lineas-t-bis.png")
