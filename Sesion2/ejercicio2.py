from math import sqrt

def calcular_media(x1, x2, x3):
    return (x1 + x2 + x3) / 3

def calcular_desviacion(x1, x2, x3, media):
    return sqrt(((x1 - media) ** 2 + (x2 - media) ** 2 + (x3 - media) ** 2) / 3)

x1 = float(input('Introduzca el numero x1: '))
x2 = float(input('Introduzca el numero x2: '))
x3 = float(input('Introduzca el numero x3: '))

media = calcular_media(x1, x2, x3)
desviacion = calcular_desviacion(x1, x2, x3, media)

print('La desviacion tipica es {}'.format(desviacion))

