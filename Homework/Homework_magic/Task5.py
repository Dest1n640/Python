class Foodinfo:
    def __init__(self, proteins, fats, carbohydrates):
        if proteins >= 0:
            self.proteins = proteins
        else:
            raise ValueError("Proteins must be a non-negative value.")
        
        if fats >= 0:
            self.fats = fats
        else:
            raise ValueError("Fats must be a non-negative value.")
        
        if carbohydrates >= 0:
            self.carbohydrates = carbohydrates
        else:
            raise ValueError("Carbohydrates must be a non-negative value.")

    def __str__(self):
        return (f"Protein amount - {self.proteins}\n"
                f"Fat amount - {self.fats}\n"
                f"Carbohydrate amount - {self.carbohydrates}")

    def __add__(self, other):
        return self.proteins + self.fats + self.carbohydrates

    def __mul__(self, n):
        return (self.proteins + self.fats + self.carbohydrates) * n

    def __truediv__(self, n):
        return (self.proteins + self.fats + self.carbohydrates) / n

    def __floordiv__(self, n):
        return (self.proteins + self.fats + self.carbohydrates) // n


# Example input and output:
# Input:
# proteins = 10.0
# fats = 20.0
# carbohydrates = 30.0
# n = 2.0

# Code execution:
proteins = float(input("Enter the protein amount: "))  # Example: 10.0
fats = float(input("Enter the fat amount: "))  # Example: 20.0
carbohydrates = float(input("Enter the carbohydrate amount: "))  # Example: 30.0
n = float(input("Enter the value of n: "))  # Example: 2.0

food = Foodinfo(proteins, fats, carbohydrates)
print(food)  # Output: Nutrition details

# Calculating the sum and performing operations with n
sum_nutrients = food + food  # Using __add__
print(f"Total sum of nutrients: {sum_nutrients}")  # Output: Sum of proteins, fats, and carbohydrates

multiplied_sum = food * n  # Using __mul__
print(f"Total sum multiplied by n: {multiplied_sum}")  # Output: Sum multiplied by n

divided_sum = food / n  # Using __truediv__
print(f"Total sum divided by n: {divided_sum}")  # Output: Sum divided by n

floor_divided_sum = food // n  # Using __floordiv__
print(f"Total sum floor-divided by n: {floor_divided_sum}")  # Output: Sum floor-divided by n
