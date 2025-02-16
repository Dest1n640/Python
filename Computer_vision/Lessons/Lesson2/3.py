def equation(a, b, c):
    d = b**2 - 4 * a * c
    if d < 0:
        return "D < 0"
    elif d >= 0:
        x1 = ((-b) + d**0.5) / (2 * a)
        x2 = ((-b) - d**0.5) / (2 * a)
        return x1, x2


file_name = "File.txt"
my_file = open(file_name, "r")
a, b, c = map(float, my_file.readline().split())
my_file.close()
print(equation(a, b, c))
