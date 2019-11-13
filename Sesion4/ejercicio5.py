import random

def version_1(matriz, m):
    traspuesta = []

    for i in range(m):
        fila_traspuesta = []

        for fila in matriz:
            fila_traspuesta.append(fila[i])
        
        traspuesta.append(fila_traspuesta)
    
    return traspuesta


def version_2(matriz):
    traspuesta = [[fila[i] for fila in matriz] for i in range(len(matriz))]

    return traspuesta

correcto_n = False
correcto_m = False

while not correcto_n or not correcto_m:
    try:
        if not correcto_n:
            n = int(input("Introduzca el valor de N: "))
            
            # Continuar si el valor es correcto
            if n > 0:
                correcto_n = True
        if not correcto_m:
            m = int(input("Introduzca el valor de M: "))
            
            # Continuar si el valor es correcto
            if m > 0:
                correcto_m = True
    except ValueError:
        print("Error. Se esperaba un valor entero")

matriz = [[random.randint(1, 10) for i in range(m)] for j in range(n)]

print("Matriz original")
for f in matriz:
    print(f)

traspuesta = version_1(matriz, m)

print("Matriz traspuesta V1")
for f in traspuesta:
    print(f)


traspuesta = version_2(matriz)

print("Matriz traspuesta V2")
for f in traspuesta:
    print(f)
