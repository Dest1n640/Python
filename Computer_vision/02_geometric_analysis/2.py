def equation(a, b, c):
    d = b**2 - 4 * a * c
    if d < 0:
        return "D < 0"
    elif d >= 0:
        x1 = ((-b) + d**0.5) / (2 * a)
        x2 = ((-b) - d**0.5) / (2 * a)
        return x1, x2


a, b, c = map(float, input("Input a, b, c: ").split())
print(equation(a, b, c))
