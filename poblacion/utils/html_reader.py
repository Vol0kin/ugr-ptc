from bs4 import BeautifulSoup
import tempfile

class HTMLReader:
    def __init__(self):
        self.html = ""
    

    def __join_names(self, cod_names):
        """
        Metodo que permite juntar los codigos y los nombres dada una lista.
        Los codigos y los nombres deben estar contiguos

        Args:
            cod_names: Lista de de codigos y nombres
        
        Returns:
            Lista con los nombres y los códigos juntos
        """
        # Juntar los elementos
        # Se reemplaza la cadena " - " por "-" para evitar problemas
        # de formato entre ficheros
        joined_str = [" ".join(cod_names[i:i+2]).replace(" - ", "-") for i in range(0, len(cod_names), 2)]

        return joined_str 
    

    def __find_all_td(self):
        """
        Metodo para encontrar todos los elementos con la etiqueta <td>...</td> 
        de una tabla y pasarlos a texto

        Returns:
            Lista con todas las celdas de la tabla en formato string
        """
        # Encontrar todos los td de la tabla
        td = self.html.find_all("td")

        # Convertir los elementos a texto
        td_str = [t.get_text() for t in td]

        return td_str
    

    def read_html(self, html_page):
        """
        Metodo para leer el contenido de una pagina web en un formato
        que no es UTF-8, pasarlo a este formato y guardarlo en el atributo
        utilizando para ello BeautifulSoup

        Args:
            html_page: Nombre del ficher que contiene la pagina web a ser procesada
        """
        # Leer el contenido original de la pagina web y guardarlo
        # El formato no es utf-8, por tanto, habra que cambiarlo
        with open(html_page, "r", encoding="ISO-8859-1") as f:
            html_content = f.read()
        
        # Guardar el contenido en un fichero temporal
        with tempfile.NamedTemporaryFile(suffix=".htm", encoding="utf-8", mode="w", delete=False) as temp:
            temp.write(html_content)
        
        # Leer el contenido del fichero temporal con el formato correcto
        # y guardarlo en el atributo con el formato de BeautifulSoup
        with open(temp.name, encoding="utf-8") as temp_html:
            self.html = BeautifulSoup(temp_html.read(), 'html.parser')
    

    def read_communities_provinces(self):
        """
        Metodo para obtener las comunidades automonas a partir de la
        pagina de entrada

        Returns:
            Diccionario con las comunidades autonomas y las provincias
            de cada una de ellas
        """
        # Obtener elementos con etiqueta <td>
        td_str = self.__find_all_td()        

        # Eliminar aquellas filas que no aportan información
        td_str = list(filter(lambda x: not x == '' and not "Ciudades" in x, td_str))

        # Juntar los nombres de las comunidades y las provincias con sus codigos
        comm_prov = self.__join_names(td_str)

        # Crear diccionario con nombres de comunidades
        dict_comm_prov = {comm_prov[i]: [] for i in range(0, len(comm_prov), 2)}

        # Rellenar las comunidades con las provincias
        for i in range(0, len(comm_prov), 2):
            dict_comm_prov[comm_prov[i]].append(comm_prov[i+1])

        return dict_comm_prov
    
    
    def read_communities(self):
        """
        Metodo para obtener las comunidades autonomas

        Returns:
            Lista con las comunidades
        """
        # Obtener elementos con etiqueta <td>
        td_str = self.__find_all_td()

        # Juntar los los codigos de las comunidades con sus nombres
        communities = self.__join_names(td_str)

        return communities