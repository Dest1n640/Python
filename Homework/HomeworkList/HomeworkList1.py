a = str(input("Введите загаданное число"))
b = str(input("Предположение чему равно это число"))
my_list1 = [int(i) for i in str(a)]
my_list2 = [int(i) for i in str(b)]
cow = 0
bull = 0
for ind1, i in enumerate(my_list1):
    for ind2,q in enumerate (my_list2):
        if my_list1[ind1] == my_list2[ind2]:
            cow+=1
for a,b in zip(my_list1, my_list2):
    if a==b:
        bull +=1
    
            
            
print(bull, cow-bull)