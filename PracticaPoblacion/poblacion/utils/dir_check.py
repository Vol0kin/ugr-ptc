import os

def check_exists_dir(dirname):
    """
    Funcion que comprueba si existe un determinado directorio, y en caso
    de que no exsita, lo crea

    Args:
        dirname: Directorio a comprobar (y crear en caso de no existir)
    """
    # Comprobar existencia del directorio
    if not os.path.exists(dirname):
        os.mkdir(dirname)