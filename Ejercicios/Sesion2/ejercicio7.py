# Entrada de datos
nombre = input('Introduzca su nombre: ')
primer_apellido = input('Introduzca el primer apellido: ')
segundo_apellido = input('Introduzca el segundo apellido: ')

# Concatenar el nombre con los apellidos
nombre_compl = nombre + " " + primer_apellido + " " + segundo_apellido

# Mostrar por pantalla el nombre completo y al revés
print('Su nombre completo es: {}'.format(nombre_compl))
print('Su nombre completo al revés es: {}'.format(nombre_compl[::-1]))

# Separar el nombre completo
nom, apel_1, apel_2 = nombre_compl.split()

# Mostrar por pantalla cada parte del nombre
print('Su nombre es {}'.format(nom))
print('Su primer apellido es {}'.format(apel_1))
print('Su segundo apellido es {}'.format(apel_2))