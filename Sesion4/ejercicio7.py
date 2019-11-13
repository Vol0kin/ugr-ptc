import random

def version_1(valores_n, valores_m):
    interseccion = []

    # Encontrar interseccion
    for v in valores_n:
        if v in valores_m and v not in interseccion:
            interseccion.append(v)
    
    num_valores = len(interseccion)

    # Ordenar valores mediante seleccion
    for i in range(num_valores):
        v = interseccion[i]
        min_idx = i
        min_val = v

        for j in range(i+1, num_valores):
            if interseccion[j] < min_val:
                min_idx = j
                min_val = interseccion[j]
        
        interseccion[i], interseccion[min_idx] = min_val, v
    
    return interseccion


def version_2(valores_n, valores_m):
    # Convertir a set
    set_n = set(valores_n)
    set_m = set(valores_m)

    # Buscar intesrseccion
    interseccion = list(set_n.intersection(set_m))

    # Ordenar interseccion
    interseccion.sort()

    return interseccion


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

interseccion_1 = version_1(valores_n, valores_m)
print("Interseccion funcion propia: {}".format(interseccion_1))

interseccion_2 = version_2(valores_n, valores_m)
print("Interseccion utilizando set: {}".format(interseccion_2))
