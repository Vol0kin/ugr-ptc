correcto = False

def version_1(n):
    # Lista vacia de factores
    factores = []

    # Primo inicial
    primo = 2

    # Copia del numero (porque se va a ir dividiendo)
    num = n
    
    while primo <= n / 2:
        while num % primo == 0:
            factores.append(primo)
            num /= primo
    
        primo += 1
    
    # Si no se ha encontrado ningun factor, es que el numero es primo
    if len(factores) == 0:
        factores.append(n)
    
    return factores

while not correcto:
    try:
        n = int(input("Introduzca el valor de N: "))
        
        # Continuar si el valor es correcto
        if n >= 1:
            correcto = True
    except ValueError:
        print("Error. Se esperaba un valor entero")

factores = version_1(n)
print("El número {} se descompone en los siguientes factores primos: {}".format(n, factores))