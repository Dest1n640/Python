class Product:
    def __init__(self, name, price, weight):
        self.__name = name
        self.__price = price
        self.__weight = weight

    def get_name(self):
        return self.__name
    def set_name(self, name):
        if not isinstance(name, str):
            raise ValueError("Name must be a string")
        self.__name = name

    def get_price(self):
        return self.__price
    def set_price(self, price):
        if price < 0:
            raise ValueError("Price cannot be less than 0")
        self.__price = price

    def get_weight(self):
        return self.__weight
    def set_weight(self, weight):
        if weight < 0:
            raise ValueError("Weight cannot be less than 0")
        self.__weight = weight

class Buy(Product):
    def __init__(self, name, price, weight, amount):
        super().__init__(name, price, weight)
        self.__amount = amount
        self.__full_price = price * amount
        self.__full_weight = weight * amount

    def get_amount(self):
        return self.__amount
    def set_amount(self, amount):
        if amount < 0:
            raise ValueError("Amount cannot be less than 0")
        self.__amount = amount
        self.__full_price = self.get_price() * amount
        self.__full_weight = self.get_weight() * amount

    def get_full_price(self):
        return self.__full_price

    def get_full_weight(self):
        return self.__full_weight


class Check(Buy):
    def __init__(self, name, price, weight, amount):
        super().__init__(name, price, weight, amount)

    def __str__(self):
        return (
            f"Product: {self.get_name()},\n "
            f"Price per unit: {self.get_price()},\n "
            f"Weight per unit: {self.get_weight()},\n "
            f"Amount: {self.get_amount()},\n "
            f"Total price: {self.get_full_price()},\n "
            f"Total weight: {self.get_full_weight()}\n"
        )

check1 = Check(name="Apple", price=2, weight=0.5, amount=10)
print(check1)
# Output:
# Product: Apple, Price per unit: 2, Weight per unit: 0.5, Amount: 10, Total price: 20, Total weight: 5.0

check2 = Check(name="Banana", price=1.5, weight=0.3, amount=15)
print(check2)
# Output:
# Product: Banana, Price per unit: 1.5, Weight per unit: 0.3, Amount: 15, Total price: