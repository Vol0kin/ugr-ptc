import os
import locale
from decimal import Decimal, getcontext

class HTMLWorker:
    def __init__(self, title):
        self.html_begin = f"""<!DOCTYPE html>
        <html>
            <head>
                <title>{title}</title>
                <link rel="stylesheet" href="../style/estilo.css">
                <meta charset="utf8">
            </head>
            <body>
                <table>
        """

        self.html_end = """
                </table>
            </body>
        </html>
        """

        locale.setlocale(locale.LC_ALL, 'es_ES.utf8')
        getcontext().prec = 2
    
    def write_HTML_output(self, output, out_file):

        # Establecer directorio de salida
        result_dir = "resultados/"

        # Crear directorio de salida en caso de que no exista
        if not os.path.exists(result_dir):
            os.mkdir(result_dir)
        
        # Escribir salida al fichero
        with open(result_dir + out_file, "w", encoding="utf-8") as f:
            f.write(output)
    
    def write_population_var_province_years(self, pop_prov_info, types, years, out_file):
        # Añadir informacion inicial a la salida
        output = self.html_begin

        """
        Escribir primera linea de la salida, donde estaran
        algunas de las cabeceras
        """
        output += """<tr>
            <th rowspan="2"></th>
        """

        # Escribir los tipos de variaciones
        for type in types:
            output += f'<th colspan="7">{type}</th>\n'
        
        output += "</tr>\n"

        """
        Escribir segunda linea de la salida, donde estaran los años
        """
        output += "<tr>\n"

        """
        Escribir los años (se repite tantas veces el numero de años como
        tipos de variacion haya
        """
        for year in years * len(types):
            output += f"<th>{year}</th>\n"
        
        output += "</tr>\n"

        """
        Escribir contenido de la tabla
        prov -> Provincias
        pop_info -> {tipo_variacion: {año: poblacion}}
        """
        for prov, pop_info in pop_prov_info.items():
            # Escribir provincia
            output += f"""<tr>
            <th>{prov}</th>
            """

            """
            Obtener años y poblacion asociada a cada año para cada tipo
            de variacion
            year_pop -> {año: poblacion} (un diccionario para cada tipo
            de variacion; dos diccionarios en total)
            """
            for year_pop in pop_info.values():
                # Obtener poblacion para cada año
                for pop in year_pop.values():
                    # Formatear salida segun el tipo y añadirla
                    if isinstance(pop, float):
                        value = locale.format_string("%.2f", Decimal(str(pop)), grouping=True)
                    else:
                        value = locale.format_string("%d", pop, grouping=True)
                    
                    output += f"<td>{value}</td>\n"

            output += "</tr>\n"
        
        output += "</tr>\n"

        # Añadir informacion final a la salida
        output += self.html_end

        # Escribir salida
        self.write_HTML_output(output, out_file)
