num1 = int(input("Input the number1: "))
num2 = int(input("Input the number2: "))

operation = input("Input the operation(+, -, *, /): ")

if operation == "+":
    print(f"Result: {num1 + num2}")
elif operation == "-":
    print(f"Result: {num1 - num2}")
elif operation == "*":
    print(f"Result: {num1 * num2}")
elif operation == "/":
    if num2 != 0:
        print(f"Result: {num1 / num2}")
    else:
        print("Error: Division by zero")
else:
    print("Error: Invalid operation")
