from utils import pop_funcs
from utils import read_csv
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

    writer.write_table(pop_community, "Población de cada comunidad autónoma entre 2010 y 2017",
                       "poblacionComAutonomas.htm", use_genders=True)

    