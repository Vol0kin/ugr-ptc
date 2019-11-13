def version_1(valores):
    num_elementos = 0
    impares = []

    for v in valores:
        if v % 2:
            impares.append(v)
            num_elementos += 1
    
    return impares, num_elementos


def version_2(valores):
    impares = list(filter(lambda x: x % 2, valores))

    return impares, len(impares)


correcto = False

while not correcto:
    try:
        n = int(input("Introduzca el valor de N: "))
        
        # Continuar si el valor es correcto
        if n >= 1:
            correcto = True
    except ValueError:
        print("Error. Se esperaba un valor entero")

valores = [i for i in range(1, n + 1)]

print("Valores: {}".format(valores))

impares_1, long_1 = version_1(valores)
print("Valores impares obtenidos por la funcion propia: ", impares_1)
print("Longitud: ", long_1)

impares_2, long_2 = version_2(valores)
print("Valores impares obtenidos con filter() y len(): ", impares_2)
print("Longitud: ", long_2)