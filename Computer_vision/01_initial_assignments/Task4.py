import random


def fractional_part(x):
    return abs(x) % 1


# Генерация списка из 10 случайных вещественных чисел
numbers = [random.uniform(-100, 100) for _ in range(10)]

if all(n == int(n) for n in numbers):
    numbers[0] += 0.1

sorted_numbers = sorted(numbers, key=fractional_part)

print("Список до сортировки:", numbers)
print("Список после сортировки:", sorted_numbers)
