import financiacion

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


    # Obtener el capital final

    capital_anual = capital

    for _ in range(anios):
        capital_anual = financiacion.calcularCapitalFinal(capital_anual, interes)

    print('El capital final al cabo de {} años es {}€'.format(anios, capital_anual))
