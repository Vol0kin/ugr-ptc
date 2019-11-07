vocales_str = "aeiouAEIOU"

def vocales(palabra):
    vocales_palabra = ""

    for c in palabra:
        if c in vocales_str:
            vocales_palabra += c

    return vocales_palabra

palabra = input("Introduzca una palabra: ")

vocs = vocales(palabra)
print("Las vocales encontradas en la palabra con la funcion propia son {}".format(vocs))

