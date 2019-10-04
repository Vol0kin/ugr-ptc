# Establecer los cc de un tercio y el limite de alcohol
CC_TERCIO = 333
CC_ALCOHOL = 50

# Entrada del porcentaje de alcohol
alchohol = float(input('Introduzca la cantidad de alcohol: '))

# Calcular la cantidad de alcohol en un tercio
cc_alc_tercio = CC_TERCIO * (alchohol / 100)

# Calcular el numero de tercios
n_tercios = int(CC_ALCOHOL / cc_alc_tercio)

# Mostrar por pantalla el resultado
print('Como mucho puedes tomarte {} tercios'.format(n_tercios))