RENDIMIENTO = 0.17
TAM = 1.6
DIAS = 30

# Entrada de datos
mean_radiacion = float(input('Introduzca la radiacion solar media: '))

kw_h_mes_panel = DIAS * mean_radiacion * RENDIMIENTO * TAM
num_paneles = int(1000 / kw_h_mes_panel) + 1

print("El número mínimo de paneles solares es: {} paneles".format(num_paneles))