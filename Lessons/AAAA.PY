# import random  #Способ 1, но лучше через генератор

# my_list = []
# n = int(input()) # Кол во строк
# m = int(input()) # Колво столбцов (элементов)
# for i in range(n):
#     row = []
#     for j in range(m):
#         row.append(random.randint(10,70))
#     my_list.append(row)
# print(my_list)



# способ 2. использование генератора +++ 
import random
n = int(input())
m = int(input())
my_list = [[random.randint (10,70) for j in range(m) ] for i in range(n)]
my_list2 = [[int(j) for j in input().split()] for i in range(n)]


print(my_list)

# Обработка элементов
# for idx_r, row in enumerate(my_list):
#     for ind, item in enumerate(row):
#         my_list[idx_r][ind-1] = item
        
# print(my_list)


# Способ обработки списка (индексы не нужны)
for row in my_list:
    for item in row:
        print(item, end=" ")
    print()
    
    
for row in my_list:
    print("{0} {1} {2} {3}".format(row))





