import random

def version_1(valores_n, valores_m):
    # Juntar valores
    valores_nm = valores_n + valores_m

    # Lista vacia con los valores unicos
    valores_nm_unicos = []

    # Valores unicos de N y M
    for v in valores_nm:
        if v not in valores_nm_unicos:
            valores_nm_unicos.append(v)
    
    # Obtener numero de elementos
    num_valores = len(valores_nm_unicos)

    # Ordenar valores mediante seleccion
    for i in range(num_valores):
        v = valores_nm_unicos[i]
        min_idx = i
        min_val = v

        for j in range(i+1, num_valores):
            if valores_nm_unicos[j] < min_val:
                min_idx = j
                min_val = valores_nm_unicos[j]
        
        valores_nm_unicos[i], valores_nm_unicos[min_idx] = min_val, v
    
    return valores_nm_unicos


def version_2(valores_n, valores_m):
    # Valores unicos
    valores_nm = list(set(valores_n + valores_m))

    # Ordenar
    valores_nm.sort()

    return valores_nm


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

valores_n = [random.randint(1, 10) for i in range(n)]
valores_m = [random.randint(1, 10) for i in range(m)]

print("N: {}".format(valores_n))
print("M: {}".format(valores_m))

valores_nm_1 = version_1(valores_n, valores_m)
print("Valores de N y M unicos y en orden ascendente mediante funcion propia: ", valores_nm_1)

valores_nm_2 = version_2(valores_n, valores_m)
print("Valores de N y M unicos y en orden ascendente mediante funciones del lenguaje: ", valores_nm_2)