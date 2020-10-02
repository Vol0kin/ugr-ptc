from math import sqrt

def calcular_media(x1, x2, x3):
    """
    Funcion que permite calcular la media de tres numeros.

    Args:
        x1: Primer numero.
        x2: Segundo numero.
        x3: Tercer numero.
    Return:
        Devuelve la media de los tres numeros de entrada.
    """
    return (x1 + x2 + x3) / 3

def calcular_desviacion(x1, x2, x3, media):
    """
    Funcion que calcula la desviacion de tres numeros, utilizando la media de
    estos.

    Args:
        x1: Primer numero.
        x2: Segundo numero.
        x3: Tercer numero.
        media: Media de los tres numeros.
    Return:
        Devuelve la desviacion tipica de los tres numeros.
    """
    return sqrt(((x1 - media) ** 2 + (x2 - media) ** 2 + (x3 - media) ** 2) / 3)

# Entrada de datos
x1 = float(input('Introduzca el numero x1: '))
x2 = float(input('Introduzca el numero x2: '))
x3 = float(input('Introduzca el numero x3: '))

# Calcular media
media = calcular_media(x1, x2, x3)

# Calcular desviacion
desviacion = calcular_desviacion(x1, x2, x3, media)

# Salida por pantalla
print('La desviacion tipica es {}'.format(desviacion))

