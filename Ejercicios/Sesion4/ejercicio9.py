import random

def version_1(valores_n, valores_m):
    diferencia = []

    # Encontrar diferencia
    for v in valores_n:
        if v not in valores_m and v not in diferencia:
            diferencia.append(v)
    
    num_valores = len(diferencia)

    # Ordenar valores mediante seleccion
    for i in range(num_valores):
        v = diferencia[i]
        min_idx = i
        min_val = v

        for j in range(i+1, num_valores):
            if diferencia[j] < min_val:
                min_idx = j
                min_val = diferencia[j]
        
        diferencia[i], diferencia[min_idx] = min_val, v
    
    return diferencia


def version_2(valores_n, valores_m):
    set_n = set(valores_n)
    set_m = set(valores_m)

    diferencia = list(set_n.difference(set_m))

    diferencia.sort()

    return diferencia

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

diferencia_1 = version_1(valores_n, valores_m)
print("Diferencia funcion propia: {}".format(diferencia_1))

diferencia_2 = version_2(valores_n, valores_m)
print("Diferencia utilizando set: {}".format(diferencia_2))