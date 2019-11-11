from . import dir_check
import locale
from decimal import Decimal, getcontext

class HTMLWriter:
    def __init__(self):
        self.html = ""

        locale.setlocale(locale.LC_ALL, 'es_ES.utf8')
        getcontext().prec = 2
    

    def __generate_years(self, upper_lim=2017, lower_lim=2010):
        """
        Metodo para generar una sucesion de años que apareceran en la tabla

        Args:
            upper_lim: Año mas grande que va a aparecer en las cabeceras
            lower_lim: Año mas pequeño que va a aparecer en las cabeceras
        """
        return [y for y in range(upper_lim, lower_lim-1, -1)]


    def __init_html(self, title):
        """
        Metodo para escribir la primera parte de la salida en HTML

        Args:
            title: Titulo que va a tener la pagina
        """
        self.html = f"""<!DOCTYPE html>
        <html>
            <head>
                <title>Información Población</title>
                <link rel="stylesheet" href="../style/estilo.css">
                <meta charset="utf8">
            </head>
            <body>
                <h1>{title}</h1>"""
    

    def __write_first_column_table(self, rowspan):
        """
        Metodo que escribe la primera columna en blanco durante un numero de
        filas determinado

        Args:
            rowspan: Numero de filas que va a ocupar la columan en blanco
        """

        self.html += f"""
                <table>
                    <tr>
                        <th rowspan="{rowspan}"></th>"""
    

    def __write_years_header(self, num_repetitions, upper_lim=2017, lower_lim=2010):
        """
        Metodo para escribir los años en la tabla un numero de veces

        Args:
            num_repetitions: Numero de veces que se escribiran los años
            upper_lim: Año mas grande que va a aparecer en las cabeceras
            lower_lim: Año mas pequeño que va a aparecer en las cabeceras
        """
        # Obtener lista con los años
        years = self.__generate_years(upper_lim=upper_lim, lower_lim=lower_lim)

        self.html += """
                    <tr>"""

        for y in years * num_repetitions:
            self.html += f"""
                        <th>{y}</th>"""
        
        self.html += """
                    </tr>"""
    

    def __write_header(self, variation=False, use_genders=False):
        """
        Metodo que escribe la cabecera de la tabla

        Args:
            variation: Indica si la tabla es de variacion (default False)
            use_genders: Indica si se tienen que utilizar generos (default False)
        
        Raises:
            AssertionError: Si los dos valores booleanos son False
        """
        # Comprobar que se ha especificado alguna opcion valida
        assert variation or use_genders, "Esperaba que alguna opcion fuese True"

        # Determinar cuanto debe ocupar el rowspan de la primera columna de la tabla
        rowspan = 3 if variation and use_genders else 2

        # Escribir primera columna en blanco
        self.__write_first_column_table(rowspan)

        # Determinar colspan base
        # Depende del tipo de tabla
        # 7 para tablas con variacion, 8 en caso contrario
        colspan_base = 7 if variation else 8

        # Escribir parte de la tabla de variacion (si se ha indicado)
        # En caso contrario escribir parte de generos
        if variation:
            # Establecer cuanto va a ocupar el colspan de la fila de la variacion
            colspan_var = 7 if not use_genders else 2 * 7

            self.html += f"""
                        <th colspan="{colspan_var}">Variación Absoulta</th>
                        <th colspan="{colspan_var}">Variación Relativa</th>
                    </tr>"""
            
            # Añadir cabeceras si se usan generos
            if use_genders:
                self.html += f"""
                    <tr>
                        <th colspan="{colspan_base}">Hombres</th>
                        <th colspan="{colspan_base}">Mujeres</th>
                        <th colspan="{colspan_base}">Hombres</th>
                        <th colspan="{colspan_base}">Mujeres</th>
                    </tr>"""
        else:
            self.html += f"""
                        <th colspan="{colspan_base}">Total</th>
                        <th colspan="{colspan_base}">Hombres</th>
                        <th colspan="{colspan_base}">Mujeres</th>
                    </tr>"""
        
        # Determianar cuantas veces se deben repetir los años
        if variation:
            if use_genders:
                years_repeat = 4
            else:
                years_repeat = 2
        else:
            years_repeat = 3        
        
        # Determinar el limite inferior de los años que se deben escribir
        lower_lim = 2011 if variation else 2010

        # Escribir los años
        self.__write_years_header(years_repeat, lower_lim=lower_lim)


    def __write_values(self, population):
        """
        Metodo que escribe los valores de la poblacion en la tabla

        Args:
            population: Poblacion a escribir
        """

        # Procesar cada area
        for area, pop in population.items():
            self.html += f"""
                    <tr>
                        <th>{area}</th>"""
            
            # Escribir cada valor de la forma correspondiente
            for p in pop.values():
                if isinstance(p, float):
                    value = locale.format_string("%.2f", Decimal(str(p)), grouping=True)
                else:
                    value = locale.format_string("%d", p, grouping=True)
                
                self.html += f"""
                        <td>{value}</td>"""
            
            self.html += """
                    </tr>"""


    def __write_close_table(self):
        """
        Metodo para escribir la el cierre de la etiqueta <table>
        """

        self.html += """
                </table>"""
    

    def __write_image(self, img_path=None):
        """
        Metodo que escribe una imagen dada una ruta, si se especifica
        alguna
        """
        # Escribir imagen si se ha especificado alguna
        if not img_path is None:
            self.html += f"""
            <img src="../{img_path}" alt="Grafico sobre población">""" 
    

    def __write_close_body_html(self):
        """
        Metodo para cerrar las etiquetas <body> y <html>
        """

        self.html += """
            </body>
        </html>
        """
    
    def __write_HTML_output(self, outfile):
        """
        Metodo para escribir la tabla generada en un fichero de salida

        Args:
            outfile: Fichero de salida
        """

        # Establecer directorio de salida
        result_dir = "resultados/"

        # Crear directorio de salida en caso de que no exista
        dir_check.check_exists_dir(result_dir)        
        
        # Escribir salida al fichero
        with open(f"{result_dir}{outfile}", "w", encoding="utf-8") as f:
            f.write(self.html)
    

    def write_table(self, population, title, output, variation=False,
                    use_genders=False, img_path=None):
        """
        Metodo para escribir una tabla sobre una poblacion

        Args:
            population: Informacion sobre la poblacion que se quiere mostrar
            title: Titulo que va a tener la pagina
            output: Archivo de salida
            variation: Indica si la tabla es de variacion (default False)
            use_genders: Indica si se tienen que utilizar generos (default False)
            img_path: Ruta de la imagen (default None)
        """
        # Inicializar HTML
        self.__init_html(title)

        # Escribir header
        self.__write_header(variation=variation, use_genders=use_genders)

        # Escribir valores
        self.__write_values(population)

        # Cerrar tabla
        self.__write_close_table()

        # Escribir imagen
        self.__write_image(img_path=img_path)

        # Cerrar body y html
        self.__write_close_body_html()

        # Escribir salida
        self.__write_HTML_output(output)
