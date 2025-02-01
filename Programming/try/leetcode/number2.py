def Add_Two_Numbers(l1, l2):
    l3 = []
    carry = 0
    max_len = max(len(l1), len(l2))
    l1 += [0] * (max_len - len(l1))
    l2 += [0] * (max_len - len(l2))
    for i in range(max_len):
        total = l1[i] + l2[i] + carry
        l3.append(total % 10)
        carry = total // 10
    if carry:
        l3.append(carry)
    return l3

l1 = [int(i) for i in input("Input l1: ").split()]
l2 = [int(i) for i in input("Input l2: ").split()]

print(Add_Two_Numbers(l1, l2))

