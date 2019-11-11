from utils import pop_funcs
from utils import read_csv
from utils import graphics
from utils.html_reader import HTMLReader
from utils.html_writer import HTMLWriter

if __name__ == "__main__":
    # Obtener datos de poblacion y claves de columnas
    population, col_keys = read_csv.read_csv_file("datos/poblacionProvinciasHM2010-17.csv")

    reader = HTMLReader()
    writer = HTMLWriter()

    ###########################################################################
    # R1
    ###########################################################################   
    print("Generando informacion sobre las variaciones medias y abosultas de la poblacion de cada provincia...")
    new_pop = pop_funcs.abs_rel_population_variance(population, col_keys)
    writer.write_table(new_pop, "Variación de la población de cada provincia entre 2011 y 2017",
                       "variacionProvincias2011-17.htm", variation=True)
    print("Información generada!")

    ###########################################################################
    # R2
    ###########################################################################
    reader.read_html("datos/comunidadesAutonomas.htm")
    communities = reader.read_communities()
    reader.read_html("datos/comunidadAutonoma-Provincia.htm")
    provinces = reader.read_communities_provinces()

    pop_community = pop_funcs.population_community(population, col_keys, communities, provinces)

    writer.write_table(pop_community, "Población de cada Comunidad Autónoma entre 2010 y 2017",
                       "poblacionComAutonomas.htm", use_genders=True)
    
    ###########################################################################
    # R3
    ###########################################################################
    most_pop_comm = pop_funcs.get_comms_most_mean_population(pop_community, col_keys)
    graphics.bar_plot_man_woman(pop_community, most_pop_comm, "graficos-barra-hm.png")
    writer.write_table(pop_community, "Población de cada comunidad autónoma entre 2010 y 2017",
                       "poblacionComAutonomas.htm", use_genders=True, img_path="resultados/graficos-barra-hm.png")
    
    ###########################################################################
    # R4
    ###########################################################################
    comm_variation = pop_funcs.abs_rel_population_variance(pop_community, col_keys, use_genders=True)
    writer.write_table(comm_variation, "Variación de la población de cada Comunidad Autónoma entre 2011 y 2017",
                       "variacionComAutonomas.htm", variation=True ,use_genders=True)