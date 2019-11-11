import csv
import tempfile
import numpy as np

def read_csv_file(file_path):
    """
    Funcion para leer un fichero .csv de entrada y obtener de el
    un diccionario que represente la informacion

    Args:
        file_path: Ruta del archivo .csv
    
    Returns:
        Diccionario con la informacion sobre la poblacion por años
        y generos para distintas zonas y una lista con las claves
        de las columnas para acceder a la informacion
    """
    # Diccionario de salida
    # El diccionario tendra la siguiente estructura:
    # {provincia: {genero-año: poblacion}}
    # Se conserva el orden de insercion
    population_dict = {}

    # Establecer opciones para leer el archivo CSV, como el delimitador
    csv.register_dialect("file_dialect", delimiter=";")
    
    # Abrir el archivo CSV en modo lectura
    # Especificar que el tipo de codificacion es ISO-8859-1
    with open(file_path, "r", encoding="ISO-8859-1") as csv_file:
        # Leer el contenido del fichero principal
        csv_content = csv_file.read()

        # Filtrar contenido para eliminar informacion no relevante (cabeceras, etc.)
        start = csv_content.find("Total")
        end = csv_content.find("Notas")

        filt_csv = csv_content[start:end]
    
    # Escribir en un fichero temporal de formato .csv el contenido filtrado en formato UTF-8
    with tempfile.NamedTemporaryFile(suffix=".csv", encoding="utf-8", mode="w", delete=False) as temp:
        temp.write(filt_csv)
    
    # Procesar el archivo temporal
    with open(temp.name, encoding="utf-8") as temp_csv:
        # Crear reader para leer el archivo de forma secuencial
        reader = csv.reader(temp_csv, dialect="file_dialect")
        
        # Funcion para filtrar valores no validos (aquellos que son '')
        filt_func = lambda x: not x == ''
        
        # Extraer el genero de los datos de poblacion (total, hombre o mujer)
        # Se extrae de la siguiente linea de la informacion cargada
        # Se eliminan aquellos valores no validos
        # Escogemos solo el primer caracter de cada genero
        gender_keys = [g[0] for g in list(filter(filt_func, next(reader)))]

        # Extraer los años en los que se ha tomado cada muestra
        # Se extraen los años de forma única, de tal forma que no haya ninguna repeticion
        # y se dejan en el mismo orden en el que aparecen (en orden decreciente)
        # Se eliminan aquellos valores no validos
        year_keys = sorted(list(set(list(filter(filt_func, next(reader))))), reverse=True)

        # Combinar generos y años en una unica clave
        gender_years_keys = [g + y for g in gender_keys for y in year_keys]

        # Procesar cada una de las filas restantes
        for row in reader:
            # Obtener la provincia
            # Es el primer dato que se puede ver en la fila
            prov = row[0]

            # Obtener la poblacion
            # Se empieza por la segunda columna; la primera es la provincia
            # La ultima columna es vacia, por tanto se ignora
            population = np.array(row[1:-1], dtype=float)

            # Añadir informacion al diccionario de poblacion
            population_dict[prov] = {gender_year: pop for gender_year, pop in zip(gender_years_keys, population)}
    
    return population_dict, gender_years_keys
