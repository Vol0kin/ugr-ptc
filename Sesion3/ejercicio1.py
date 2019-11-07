def contar_letras(palabra, letra):
    num_apariciones = 0

    for caracter in palabra:
        if caracter == letra:
            num_apariciones += 1

    return num_apariciones

palabra = input("Introduzca la palabra: ")
letra = input("Introduzca la letra que quiere buscar en la palabra: ")

num_apariciones = contar_letras(palabra, letra)

print("Usando nuestra funcion, la letra {} aparece {} veces".format(letra, num_apariciones))

num_apariciones = palabra.count(letra)

print("Usando el metodo count(), la letra {} aparece {} veces".format(letra, num_apariciones))
