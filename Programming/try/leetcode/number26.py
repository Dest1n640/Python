def number27(arr):
    amount = 0
    for _, i in enumerate(arr):
        for ind2, q in enumerate(arr):
            if i == q and i or q != _:
                q = _
                amount += 1
    return amount, arr.sort()


arr = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
print(number27(arr))
