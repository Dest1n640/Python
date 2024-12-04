a = int(input("Введите количество выборов: ")) 
my_dict = {}

for i in range(a):
    key, value = input().split() 
    value = int(value) 
    
    if key in my_dict:
        my_dict[key] += value
    else:
        my_dict[key] = value 
        
for key in sorted(my_dict):
    print(key, my_dict[key])
    
# INPUT
# McCain 10
# McCain 5
# Obama 9
# Obama 8
# McCain 1
# OUTPUP:   
# McCain 16 (10+5+1)
# Obama 17 (9+8)