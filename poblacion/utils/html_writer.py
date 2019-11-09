def write_population_var_province(pop_prov_info, out_file):
    # Establecer elementos iniciales del HTML de salida
    out_html = """<!DOCTYPE html>
    <html>
        <head>
            <title>Variación población provincias 2011-2017</title>
            <link rel="stylesheet" href="style/estilo.css">
            <meta charset="utf8">
        </head>
        <body>
            <table>
                <tr>

    """

    # Establecer elementos finales del HTML de salida
    out_html += """
            </table>
        </body>
    </html>
    """
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(out_html)