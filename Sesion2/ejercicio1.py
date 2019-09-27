precio_bruto = float(input('Introduzca el precio bruto: '))
porc_ganancia = float(input('Introduzca el porcentaje de ganancia del vendedor: '))
iva = float(input('Introduzca el porcentaje de IVA: '))

precio_base = precio_bruto * (1 + porc_ganancia / 100)
precio = precio_base * (1 + iva / 100)

print('El precio final del vehiculo es {} euros'.format(precio))
