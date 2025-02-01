my_str = input("Введите символы(>,<,-): ")
my_list = [str(i) for i in str(my_str)]
count = 0
for ind, i in enumerate(my_list):
    if my_list[ind] == ">" and my_list[ind-1] == "-" and my_list[ind-2] =="-"  and my_list[ind - 3] == ">" and my_list[ind-4] == ">":
        count+=1 
    if my_list[ind] == "<" and my_list[ind-1] == "<" and my_list[ind-2] == "-" and my_list[ind - 3] == "-" and my_list[ind-4] == "<":
        count +=1
print(count)