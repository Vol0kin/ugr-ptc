import decimal
from decimal import Decimal, getcontext

x = Decimal('0.1')

suma = x + x + x

print(suma)

if suma == Decimal('0.3'):
    print("Son iguales")
else:
    print("No son iguales")

y = Decimal('523.348')
print(y)

# Se pueden operar con ints, no con floats
x2 = y * 4

print(x2)


