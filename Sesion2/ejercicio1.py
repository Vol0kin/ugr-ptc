# Entrada de datos
precio_bruto = float(input('Introduzca el precio bruto: '))
porc_ganancia = float(input('Introduzca el porcentaje de ganancia del vendedor: '))
iva = float(input('Introduzca el porcentaje de IVA: '))

# Calculo del precio base
precio_base = precio_bruto * (1 + porc_ganancia / 100)

# Calculo del precio total
precio = precio_base * (1 + iva / 100)

# Salida por pantalla
print('El precio final del vehiculo es {} euros'.format(precio))
