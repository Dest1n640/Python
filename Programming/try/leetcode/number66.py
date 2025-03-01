def number66(digits):
    if digits[-1] == 9 and len(digits) == 1:
        digits.insert(0, 0)
    if digits[-1] == 9:
        digits[-1] = 0
        digits[-2] += 1
    else:
        digits[-1] += 1
    return digits


digits = [1, 2, 3]
print(number66(digits))
