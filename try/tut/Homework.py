#4
# a = int(input())
# if a < 18:
#     print("Доступ запрещен")
# else:
#     print("Доступ разрешен")

#6
# a = int(input())
# if a <= 13:
#     print("Детсво")
# elif a >= 14 and a <= 23:
#     print("Молодость")
# elif a >=25 and a <=59:
#     print("Зрелость")
# elif a >= 60:
#     print("Старость")
    
#7
# a, b, c = map(int, input().split())
# if a > 0 and b > 0 and c > 0:
#     print(a+b+c)
# elif a > 0 and b > 0:
#     print(a + b)
# elif a > 0 and c > 0:
#     print(a + c)
# elif b > 0 and c > 0:
#     print(b + c)
# elif b > 0:
#     print(b)
# elif a > 0:
#     print(a)
# elif c > 0:
#     print(c)
# else:
#     print(0)

#9
# a = int(input())
# if a <= 12:
#     if  a == 1 or a == 3 or a == 5 or a == 7 or a == 8 or a == 10 or a == 12:
#         print(31)
#     elif a == 4 or a == 6 or a == 9 or a == 11:
#         print(30)
#     else:
#         print(29)   Календарь на этот год

#10
# a = int(input())
# if a < 60:
#     print("Легкий вес")
# elif a >= 60 and a < 64:
#     print("Первый полусредний вес")
# elif a >= 64 and a < 69:
#     print("Полусредний вес")
  
#11
# num1 = int(input())
# num2 = int(input())
# math = input("+, -, /, *")
# if math =="+":
#     print(num1 + num2)
# elif math == "-":
#     print(num1 - num2)
# elif math == "/":
#     if num2 == 0:
#         print("НА ноль делить нельзя")
#     else:
#         print(num1 / num2)
# elif math == "*":
#     print(num1 * num2) 

#12
# a = input()
# b = input()
# if a == "желтый" and b == "красный" or a == "красный" and b == "желтый":
#     print("Оранжеый")
# elif a == "красный" and b == "синий" or a == "синий" and b == "красный":
#     print("Фиолетовый")
# elif a == "синий" and b == "желтый" or a == "желтый" and b == "синий":
#     print("Зеленый")
# else:
#     print("Ошибка цвета")

#13
# a = int(input())
# if a >= 1 and a <= 10:
#     if a%2 == 0:
#         print("Черный")
#     else:
#         print("Красный")
# elif a >= 11 and a <=18:
#     if a % 2 == 0:
#         print("Красный")
#     else:
#         print("Черный")
# elif a >=19 and a <= 28:
#     if a % 2 == 0:
#         print("Черный")
#     else:
#         print("Красный")
# elif a >=29 and a <= 36:
#     if a % 2 == 0:
#         print("Красный")
#     else:
#         print("Черный")
# elif a == 0:
#     print("Зеленый")
# else:
#     print("Ошибка ввода")
    

