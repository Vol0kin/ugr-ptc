def mayusculas_minusculas(palabra):
    return None

palabra = input("Introduzca una palabra: ")

new_palabra = mayusculas_minusculas(palabra)
print("El resultado es {}".format(new_palabra))

new_palabra = palabra.swapcase()
print("El resultado obtenido con el metodo swapcase() es {}".format(new_palabra))


