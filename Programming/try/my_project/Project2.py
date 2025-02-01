#Камень ножинцы бумага
import random
random_num = random.randint(1,3)
if random_num == 1:
    random_num = "КАМЕНЬ"
elif random_num == 2:
    random_num = "НОЖНИЦЫ"
elif random_num == 3:
    random_num = "БУМАГА"
input = input("Введите что хотите выбросить(КАМЕНЬ, НОЖНИЦЫ, БУМАГА): ")
print(f"РОБОТ ВЫБРАЛ {random_num}")
input.upper()
if input == "КАМЕНЬ":
    if random_num == "КАМЕНЬ":
        print("draw")
    elif random_num == "НОЖНИЦЫ":
        print("win")
    elif random_num =="БУМАГА":
        print("lose")
elif input == "НОЖНИЦЫ":
    if random_num == "КАМЕНЬ":
        print("lose")
    elif random_num == "НОЖНИЦЫ":
        print("draw")
    elif random_num == "БУМАГА":
        print("win")
elif input == "БУМАГА":
    if random_num == "БУМАГА":
        print("draw")
    elif random_num == "КАМЕНЬ":
        print("win")
    elif random_num == "НОЖНИЦЫ":
        print("lose")
else:
    print("Неправильный вввод")