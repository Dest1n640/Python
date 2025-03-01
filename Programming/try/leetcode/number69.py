def pow(base, exp):
    result = 1
    negative_exp = exp < 0
    exp = abs(int(exp))  # Обрабатываем только целые степени

    for _ in range(exp):
        result *= base

    return 1 / result if negative_exp else result


def sqrt(x, epsilon=1e-6):
    if x < 0:
        raise ValueError("Квадратный корень из отрицательного числа не определён")

    guess = x
    while abs(guess * guess - x) > epsilon:
        guess = (guess + x / guess) / 2  # Метод Ньютона

    return guess


# Примеры использования:
print(sqrt(4))  # 2.0
print(sqrt(9))  # 3.0
print(sqrt(16))  # 4.0
print(sqrt(2))  # 1.414...
