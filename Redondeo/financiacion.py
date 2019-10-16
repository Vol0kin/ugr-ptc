def redondear(numero, decimales):
    """
    Funcion que redondea un numero de coma flotante utilizando un numero de
    decimales en concreto

    Args:
        numero: Numero de coma flotante a redondear
        decimales: Numero de cifras decimales que usar para redondear
    Return:
        Devuelve el número redondeado con el número de cifras decimales especificadas
    """
    # Determinar el valor por el que hay que multiplicar el numero para que
    # se conserve el numero de cifras decimales especificadas al redondear
    # Es un multiplo de 10, determinado por el valor de decimales
    multiplicador = 10 ** decimales

    # Multiplicar el numero dado
    numero_mult = numero * multiplicador

    # Incrementar en 0.5 el numero multiplicado para ver si cambia
    numero_mult += 0.5

    # Convertir a entero el numero resultante
    numero_int = int(numero_mult)

    # Convertir de nuevo a coma flotante dividiendo entre el multiplicador
    numero_redondeo = numero_int / multiplicador

    return numero_redondeo


def calcularCapitalFinal(capitalInicial, interes):
    """
    Funcion que calcula el capital final dado un capital inicial y el interes anual

    Args:
        capitalInicial: Cantidad de dinero inicial
        interes: Porcentaje de incremento del capital de forma anual
    Return:
        Devuleve el capital final calculado a partir del capital inicial y
        el interes
    """
    # Calcular cuantos euros de interes anual se obtienen
    euros_interes_anual = capitalInicial * interes / 100

    # Calcular el capital final
    capital_final = capitalInicial + euros_interes_anual

    # Redondear el capital final para que tenga 2 decimales
    capital_final = redondear(capital_final, 2)

    return capital_final

