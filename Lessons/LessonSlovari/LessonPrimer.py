# river = {i:i**4 for i in range(4)}
# for key in river:
#     print(key, river[key])
    
# print(river.items())
# for key, value in river.items():
#     print(key,value)
    
# for key in river.keys():
#     print(key, river[key])
    
# for value in river.values():
#     print(value)



# Добавление в словарь
river = {i:i**4 for i in range(4)}
river.update({5:625})
print(river)



print(river.get(2,True))
print(river.get(10,False))
#Поиск значения по ключу







