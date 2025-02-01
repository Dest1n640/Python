def Roman_to_Integer(my_str, symbols, values):
    output = 0
    value_map = dict(zip(symbols, values))
    for i in my_str:
        if i in value_map:
            output += value_map[i]
    return output

symbols = ['I', 'V', 'X', 'L', 'C', 'D', 'M']
values = [1, 5, 10, 50, 100, 500, 1000]
my_str = input("Enter a Roman numeral: ")

print(Roman_to_Integer(my_str, symbols, values))

