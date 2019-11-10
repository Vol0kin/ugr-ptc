import var_poblacion_prov as r1
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
    print("Generando informacion sobre las variaciones medias y abosultas de la poblacion de cada provincia...")
    new_pop = r1.abs_rel_population_variance(population, col_keys)
    writer.write_variation_table(new_pop, "Variacion de la población de cada provincia entre 2011 y 2017", "variacionProvincias2011-17.htm")
    print("Información generada!")

    reader = HTMLReader()
    reader.read_html("datos/comunidadAutonoma-Provincia.htm")
    print(reader.read_communities_provinces())