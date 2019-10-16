import decimal
from decimal import Decimal, getcontext

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
    # Redondear utilizando la funcion quantize de decimal con el numero de
    # cifras decimales especificado en decimales
    numero_redondeo = numero.quantize(Decimal('1.' + '0' * decimales))

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


if __name__ == '__main__':
    # Entrada del capital hasta que tenga un valor valido
    capital = 0.0

    while capital <= 0.0:
        capital = float(input('Introduzca el capital inicial: '))

    # Entrada del interes hasta que tenga un valor valido
    interes = 0.0

    while interes <= 0.0:
        interes = float(input('Introduzca el interes anual: '))


    # Entrada del numero de años hasta que tenga un valor valido
    anios = 0

    while anios <= 0:
        anios = int(input('Introduzca el numero de años: '))


    # Crear un objeto decimal que contiene el capital
    capital_anual = Decimal(str(capital))

    # Crear un objeto decimal quecontiene el interes
    interes_anual = Decimal(str(interes))

    # Establecer que se tiene que hacer un redonde a partir del .5
    getcontext().rounding = decimal.ROUND_HALF_UP

    # Obtener el capital final
    for _ in range(anios):
        capital_anual = calcularCapitalFinal(capital_anual, interes_anual)

    print('El capital final al cabo de {} años es {}€'.format(anios, capital_anual))
