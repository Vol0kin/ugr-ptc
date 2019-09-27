
def normalizar_sexagesimal(tiempo):
    tiempo_normalizado = tiempo % 60
    resto = tiempo // 60

    return tiempo_normalizado, resto

def normalizar_horas(horas):
    return horas % 24

horas = int(input('Introduzca las horas: '))
minutos = int(input('Introduzca los minutos: '))
segundos = int(input('Introduzca los segundos: '))

# Normalizar los segundos y obtener el tiempo sobrante
segundos_final, resto = normalizar_sexagesimal(segundos)

# Incrementar los minutos de ser necesario y normalizarlos
minutos += resto
minutos_final, resto = normalizar_sexagesimal(minutos)

# Incrementar las horas de ser necesario y normalizarlas
horas += resto
horas_final = normalizar_horas(horas)

print('El tiempo final es: {}h {}min {}s'.format(horas_final, minutos_final, segundos_final))
