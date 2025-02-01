#Генератор случайных паролей
import random
import string

random_numbers = "".join(random.choices("0123456789", k=random.randint(1,9)))
random_str = "".join(random.choices(string.ascii_letters + string.digits, k = random.randint(1,12)))
print(random_str)


#import random
# import string

# def generate_password(length=12):
#     return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length))

# password = generate_password(16)  # генерируем пароль длиной 16 символов
# print(password)
