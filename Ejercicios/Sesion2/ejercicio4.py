precio = float(input('Introduzca el precio total: '))
cantidad = float(input('Introduzca la cantidad entregada por el cliente: '))

resto = cantidad - precio

monedas_1_euro = 0
monedas_50_cent = 0
monedas_10_cent = 0
monedas_1_cent = 0

monedas_1_euro = int(resto)
resto -= monedas_1_euro
resto = round(resto, 2)

monedas_50_cent = int(resto / 0.5)
resto -= monedas_50_cent * 0.5
resto = round(resto, 2)

monedas_10_cent = int(resto / 0.1)
resto -= monedas_10_cent * 0.1
resto = round(resto, 2)

monedas_1_cent = int(resto / 0.01)

print('Se tiene que devolver la siguiente cantidad de monedas:')
print('- {} monedas de 1 euro'.format(monedas_1_euro))
print('- {} monedas de 50 centimos'.format(monedas_50_cent))
print('- {} monedas de 10 centimos'.format(monedas_10_cent))
print('- {} monedas de 1 centimo'.format(monedas_1_cent))
