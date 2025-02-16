def number20(str):
    amount = 0
    answer = 0
    for i in str:
        if i == "(" or i == "[" or i == "{":
            amount += 1
    for i in str:
        for q in str:
            if i == "(" and q == ")":
                answer += 1
            elif i == "{" and q == "}":
                answer += 1
            elif i == "[" and q == "]":
                answer += 1
    if answer == amount:
        return True
    else:
        return False


string = "(}"
print(number20(string))
