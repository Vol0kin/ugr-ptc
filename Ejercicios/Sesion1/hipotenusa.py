from math import sqrt

a = float(input('Introduzca la longitud del primer cateto: '))
b = float(input('Introduzca la longitud del segundo cateto: '))

hipotenusa = sqrt(a ** 2 + b ** 2)

print('La hipotenusa es {}'.format(hipotenusa))
