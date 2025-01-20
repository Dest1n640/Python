def Merge_Two_Sorted_Lists(list1, list2):
    new_list = []
    for i in list1: 
        for q in list2:
            if i < q: 
                new_list.append(i)
                list1.remove(list1[i])
            else:
                new_list.append(list2[q])
                list2.remove(q)
    return new_list

list1 = [int(i) for i in input().split()]
list2  = [int(i) for i in input().split()]
print(Merge_Two_Sorted_Lists(list1, list2))
