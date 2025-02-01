import random #Угадывание числа

number = random.randint(1, 100)
help = input("Хотите подсказку(да, нет): ")
if help == 'да':
    print(number)
a = int(input("Отгадайте число от 1 до 100: "))
while number != a:
    a = int(input("Отгадайте число от 1 до 100: "))
print(f"Вы угадали - {number}")
