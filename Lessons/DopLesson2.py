# n, m = map(int, input().split())
# my_list = [[0 for i in range(m)]for i in range(n)]

# for i, row in enumerate(my_list):
#     for j, item in enumerate(row):
#         if i == j:
#             my_list[i][j] = 1
#         elif i > j:
#             my_list [i][j] = 2
#         else:
#             my_list [i][j] = 0
           
           
# for row in my_list:
#     print(*row)
 
 
 

# n, m = map(int, input("Введите количество строк и столбцов через пробел: ").split())

# my_list = [[int(i) for i in range(m)] for i in range(n)]

# count = 1
# is_num = True 

# for row in range(n):
#     for item in range(m):
#         if is_num == True:
#             my_list[row][item] = count
#             is_num = False
#             count+=1
#         elif is_num == False:
#             is_num = True
#             my_list[row][item] = 0
            


# for row in my_list:
#     print(*row)

            
            
            
            
            
            
a = input()
matr = []

while a!= "end":
    matr.append(a)
    a = input()

for ind ,row in enumerate(matr):
    matr [ind] = [int(i) for i in row.split()]
print(matr)


n = len(matr)
m = len(matr[0])

temp_matr = [[0 for i in range(m)] for i in range(n)]

