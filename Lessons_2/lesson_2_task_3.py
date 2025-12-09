import math


def square(side):
    return math.ceil(side*side)


num_side = float(input("Введите число одной стороны квадрата: "))
print(f"Плащадь квадрата равна: {square(num_side)}")
