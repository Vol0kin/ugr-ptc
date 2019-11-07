def eliminar_letras(palabra, letra):
    new_palabra = ""

    for caracter in palabra:
        if caracter != letra:
            new_palabra += caracter

    return new_palabra

palabra = input("Introduzca una palabra: ")
letra = input("Introduzca la letra que quiere eliminar: ")

new_palabra = eliminar_letras(palabra, letra)

print("Usando nuestra funcion, la palabra resultante es {}".format(new_palabra))

new_palabra = palabra.replace(letra, "")

print("Usando el metodo replace(), la palabra resultante es {}".format(new_palabra))
