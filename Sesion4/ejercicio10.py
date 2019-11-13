def version_1(frase):
    # Eliminar espacios
    frase_no_space = frase.replace(' ', '')

    # Lista vacia que contendra las letras
    letras = []

    # Obtener letras
    for l in frase_no_space:
        if not l in letras:
            letras.append(l)
    
    num_letras = len(letras)

    # Ordenar letras mediante seleccion
    for i in range(num_letras):
        l = letras[i]
        min_idx = i
        min_val = ord(l)

        for j in range(i+1, num_letras):
            if ord(letras[j]) < min_val:
                min_idx = j
                min_val = ord(letras[j])
        
        letras[i], letras[min_idx] = letras[min_idx], l
    
    # Obtener frecuencias
    frec_dict = {l: 0 for l in letras}

    for l in frase_no_space:
        frec_dict[l] += 1
    
    # Convertir a lista de tuplas
    letras_frec = [(l, f) for l, f in frec_dict.items()]

    return letras_frec


def version_2(frase):
    # Obtener letras
    letras = list(set(frase.replace(' ', '')))

    # Ordenarlas
    letras.sort()

    # Obtener frecuencias
    frecuencias = list(map(lambda x: frase.count(x), letras))
    letras_frec = [(l, f) for l, f in zip(letras, frecuencias)]

    return letras_frec

frase = input("Introduzca una frase: ")


letras_frec_1 = version_1(frase)
print("Frecuencia de cada letra con funcion propia: {}".format(letras_frec_1))

letras_frec_2 = version_2(frase)
print("Frecuencia de cada letra utilizando set: {}".format(letras_frec_2))