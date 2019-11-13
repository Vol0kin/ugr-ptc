import math

def version_1(valores):
    v_max = valores[0]
    v_min = valores[0]

    idx_max = 0
    idx_min = 0

    for i in range(len(valores)):
        if valores[i] > v_max:
            v_max = valores[i]
            idx_max = i
        elif valores[i] < v_min:
            v_min = valores[i]
            idx_min = i
    
    return v_max, idx_max, v_min, idx_min
            


def version_2(valores):
    v_max = max(valores)
    v_min = min(valores)

    idx_max = valores.index(v_max)
    idx_min = valores.index(v_min)

    return v_max, idx_max, v_min, idx_min

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

max_1, idx_max_1, min_1, idx_min_1 = version_1(valores)
print("Valor maximo encontrado en la posicion {} por la funcin propia: {}".format(idx_max_1, max_1))
print("Valor minimo encontrado en la posicion {} por la funcion propia: {}".format(idx_min_1, min_1))

max_2, idx_max_2, min_2, idx_min_2 = version_1(valores)
print("Valor maximo encontrado en la posicion {} por funciones del lenguaje: {}".format(idx_max_2, max_2))
print("Valor minimo encontrado en la posicion {} por funciones del lenguaje: {}".format(idx_min_2, min_2))