import financiacion

if __name__ == '__main__':
    # Entrada del capital hasta que tenga un valor valido
    capital = 0.0

    while capital <= 0.0:
        try:
            capital = float(input('Introduzca el capital inicial: '))

            capital_split = str(capital).split('.')

            if len(capital_split) > 1:
                if len(capital_split[1]) > 2:
                    capital = 0.0
        except ValueError:
            print("Formato incorrecto")
            capital = 0.0

    # Entrada del interes hasta que tenga un valor valido
    interes = 0.0

    while interes <= 0.0:
        try:
            interes = float(input('Introduzca el interes anual: '))
        except ValueError:
            print("Formato incorrecto")
            interes = 0.0


    # Entrada del numero de años hasta que tenga un valor valido
    anios = 0

    while anios <= 0:
        try:
            anios = int(input('Introduzca el numero de años: '))
        except ValueError:
            print("Formato incorrecto")
            anios = 0


    # Obtener el capital final

    capital_anual = capital

    for _ in range(anios):
        capital_anual = financiacion.calcularCapitalFinal(capital_anual, interes)

    print('El capital final al cabo de {} años es {}€'.format(anios, capital_anual))
