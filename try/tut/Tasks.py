def first_task():
    my_list = [int(i) for i in input().split()]
    if len(my_list) != len(set(my_list)):
        return True
    else:
        return False

def secon_task():
    s = input()
    t = input()
    s.lower()
    t.lower()
    if set(s) == set(t):
        return True
    else:
        return False
def third_task():
    my_list = [int(i) for i in input().split()]
    return my_list*2
# def forth_task():
#     my_list = [int(i) for i in input().split()]
    
def fifth_task():
    s = input()
    t = input()
    count = 0
    for ind, i in enumerate(s):
        for ind1, q in enumerate(t):
            if i == q:
                count += 1
    if count == len(t) or count == len(s):
        return True
    return False
def sixth_task():
    s = input()
    my_list = []
    my_list = s.split()
    return len(my_list[-1])
        
def seventh_task():
    nums = [int(i) for i in input().split()]
    num_map = {}
    target = input()
    for i, num in enumerate(nums):
        complement = target - num  
        if complement in num_map:
            return [num_map[complement], i]  
        num_map[num] = i
# def eigth_task():
#     strs = [str(i) for i in input().split()]
#     for ind, i in enumerate(strs):
#         for ind1, q  in enumerate(i):
        