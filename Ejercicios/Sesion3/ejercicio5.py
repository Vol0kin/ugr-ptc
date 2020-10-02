vocales = "aeiouAEIOU"

def num_vocales(palabra):
    vocs = 0

    for caracter in palabra:
        if caracter in vocales:
            vocs += 1

    return vocs

palabra = input("Introduzca la palabra: ")
vocs = num_vocales(palabra)

print("El numero de vocales con la funcion propia es {}".format(vocs))

