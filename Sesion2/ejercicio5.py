def convertir_segundos(h, mins, seg):
	return h * 3600 + mins * 60 + seg

# Entrada de datos
instante1 = input('Introduzca un instante de tiempo en formato hh:min:seg : ')
instante2 = input('Introduzca un segundo instante de tiempo en el mismo formato: ')

# Obtener las horas, minutos y segundos
h1, min1, seg1 = map(int, instante1.split(':'))
h2, min2, seg2 = map(int, instante2.split(':'))

# Calcular instantes de tiempo en segundos
t1 = convertir_segundos(h1, min1, seg1)
t2 = convertir_segundos(h2, min2, seg2)

# Calcular diferencia
t_res = t1 - t2

# Comprobar que la diferencia no sea negativa
if t_res < 0:
	t_res = 24 * 3600 + t_res

# Obtener las diferencias
h_res = t_res // 3600
t_res -= h_res * 3600

min_res = t_res // 60
t_res -= min_res * 60

seg_res = t_res

# Mostrar salida por pantalla
print('La diferencia es: {}:{}:{}'.format(h_res, min_res, seg_res))

