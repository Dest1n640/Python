from math import tan, sqrt, e


def f(x, y):
    answer = x * (e**3) + tan(sqrt(abs(x - y)))
    return answer


x, y = 5, 10
print(f(x, y))
