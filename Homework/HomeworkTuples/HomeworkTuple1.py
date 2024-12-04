w,h = map(int, input().split())

print("Ведите элементы(1,0 без пробела)")
my_tuple1=[tuple(int(i) for i in input()) for j in range(h)]
my_tuple2=[tuple(int(i) for i in input()) for j in range(h)]

my_list=[int(i) for i in input()]

def f(a,b):
    if a==0 and b==0:
        return my_list[0]
    if a==0 and b==1:
        return my_list[1]
    if a==1 and b==0:
        return my_list[2]
    elif a==1 and b==1:
        return my_list[3]

for i in range(h):
    print(*tuple(f(my_tuple1[i][j],my_tuple2[i][j]) for j in range(w)),sep='')
    