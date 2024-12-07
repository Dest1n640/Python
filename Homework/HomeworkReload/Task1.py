from functools import singledispatchmethod

class Negator:
    @singledispatchmethod
    def __init__(self, number):
        raise NotImplemented
    @__init__.register(int | float)
    def neg(self, number):
        self.number = number * (-1)

    @__init__.register(bool)
    def neg(self, number):
        self.number = not number

    @__init__.register(list | str | tuple | dict)
    def neg(self, numbers):
        raise TypeError("The passed type argument is not a justification")

    def __str__(self):
        return f"Number: {self.number}"
number1 = Negator(10)
number2 = Negator(-10.5)
number3 = Negator(True)
number4 = Negator(False)
print(number1)
print(number2)
print(number3)
print(number4)

#for error^
# number5 = Negator("1")
# print(number5)
# number6 = Negator([1])
# print(number6)
# number7 = Negator((1))
#print(number7)