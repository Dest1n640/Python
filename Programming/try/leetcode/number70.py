def climbStairs(n):
    amount = 0
    for i in range(2, n + 1):
        if i % 2 == 0:
            amount += 2
        else:
            amount += 1
    return amount


n = 5

print(climbStairs(n))  # Не работает
