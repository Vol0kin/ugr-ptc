
def max_3(x1, x2, x3):
	if x1 > x2 and x1 > x3:
		return x1
	elif x2 > x1 and x2 > x3:
		return x2
	else:
		return x3

def min_3(x1, x2, x3):
	if x1 < x2 and x1 < x3:
		return x1
	elif x2 < x1 and x2 < x3:
		return x2
	else:
		return x3


x1 = float(input('Introduzca el numero x1: '))
x2 = float(input('Introduzca el numero x2: '))
x3 = float(input('Introduzca el numero x3: '))

max_val = max_3(x1, x2, x3)
min_val = min_3(x1, x2, x3)

print('El valor mínimo es {}'.format(min_val))
print('El valor máximo es {}'.format(max_val))
