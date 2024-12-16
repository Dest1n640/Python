my_dict = input().split()
for i in my_dict:
    if i.isalnum() == False:
        del i

a = {j:my_dict.count(j) for j in my_dict}
print(a.values())

for key, value in a():
    countmax = max(a.values())
    countmin = min(a.values())
    if value == countmax:
        print(key)
    if value == countmin:
        print(key)
