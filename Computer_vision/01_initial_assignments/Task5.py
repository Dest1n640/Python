file_name = "lorem.txt"
with open(file_name, "r") as file:
    content = file.read()

    # Инициализируем словарь с буквами английского алфавита
    alphabet_dict = {chr(i): 0 for i in range(97, 123)}  # Своровал в интернете

    for char in content:
        if char in alphabet_dict:
            alphabet_dict[char] += 1

print(alphabet_dict)
