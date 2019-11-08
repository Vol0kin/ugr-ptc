import csv
import tempfile
import numpy as np

def read_csv_file(file_path):
    # Diccionario de salida
    # El diccionario tendra la siguiente estructura:
    # {provincia: {genero: {año: poblacion}}}
    population_dict = {}

    # Establecer opciones para leer el archivo CSV, como el delimitador
    csv.register_dialect("file_dialect", delimiter=";")
    
    # Abrir el archivo CSV en modo lectura
    # Especificar que el tipo de codificacion es ISO-8859-2
    with open(file_path, "r", encoding="ISO-8859-2") as csv_file:
        # Leer el contenido del fichero principal y filtrar las primeras lineas
        # Estas lineas solo contienen informacion extra
        csv_content = csv_file.read()

        start = csv_content.find("Total")
        end = csv_content.find("Notas")

        filt_csv = csv_content[start:end]
    
    # Escribir en un fichero temporal de formato .csv el contenido filtrado
    # del CSV original, en formato UTF-8
    with tempfile.NamedTemporaryFile(suffix=".csv", encoding="utf-8", mode="w", delete=False) as temp:
        temp.write(filt_csv)
    
    # Procesar el archivo temporal
    with open(temp.name) as temp_csv:
        # Crear objeto para leer el archivo de forma secuencial
        reader = csv.reader(temp_csv, dialect="file_dialect")
        
        # Funcion para filtrar valores no validos (aquellos que son '')
        filt_func = lambda x: not x == ''
        
        # Extraer el genero de los datos de poblacion (total, hombre o mujer)
        # Se extrae de la siguiente linea de la informacion cargada
        # Se eliminan aquellos valores no validos
        gender_keys = list(filter(filt_func, next(reader)))

        # Extraer los años en los que se ha tomado cada muestra
        # Se extraen los años de forma única, de tal forma que no haya ninguna repeticion
        # y se dejan en el mismo orden en el que aparecen (en orden decreciente)
        # Se eliminan aquellos valores no validos
        year_keys = sorted(list(set(map(int, list(filter(filt_func, next(reader)))))), reverse=True)

        # Procesar cada una de las filas restantes
        for row in reader:
            # Obtener la poblacion para cada año y para cada tipo de genero
            # Se transforman los valores a float y se separan en N grupos segun
            # el numero de generos que haya
            # Se empieza desde la segunda posicion (se ignora la provincia) hasta 
            # el penultimo elemento (el ultimo elemento tiene un valor de '')
            population_years_genders = np.array_split(list(map(float, row[1:-1])), len(gender_keys))

            # Crear diccionario que contiene los numeros de habitantes por año
            # segun el genero
            gender_pop = {gender: pop for gender, pop in zip(gender_keys, population_years_genders)}
            
            # Añadir al diccionario de poblacion, segun la provincia,
            # un diccionario con la poblacion por año por genero
            population_dict[row[0]] = {gender: {year: pop for year, pop in zip(year_keys, gender_pop[gender])}
                                       for gender in gender_keys}
    
    return population_dict
