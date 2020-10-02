def version_1(valores):
    suma = 0

    for v in valores:
        suma += v
    
    return suma


def version_2(valores):
    return sum(valores)
    
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

suma_1 = version_1(valores)
print("Suma de los valores obtenidos con la funcion propia: ", suma_1)

suma_2 = version_2(valores)
print("Suma de los valores obtenidos con sum(): ", suma_2)