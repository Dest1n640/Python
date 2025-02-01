class User:
    def __init__(self, name, age):
        if any(char.isdigit() for char in name):
            raise ValueError("Invalid name")
        else:
            self.name = name

        if not isinstance(age, int) or age < 0 or age > 110:
            raise ValueError("Invalid age")
        else:
            self.age = age

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if any(char.isdigit() for char in new_name):
            raise ValueError("Invalid name")
        else:
            self._name = new_name

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, new_age):
        if not isinstance(new_age, int) or new_age < 0 or new_age > 110:
            raise ValueError("Invalid age")
        else:
            self._age = new_age

    def __str__(self):
        return f"User's name - {self.name}, user's age - {self.age}"

# Example input and output:
# Input:
# name1 = "Alice"
# age1 = 30
# new_name1 = "Bob"
# new_age1 = 40

# Code execution:
name1 = input("Enter the user's name - ")  # Example: Alice
age1 = int(input("Enter the user's age - "))  # Example: 30
first_user = User(name1, age1)
print(first_user)  # Output: User's name - Alice, user's age - 30

# Asking for the second user's details
new_name1 = input("Enter a new name - ")  # Example: Bob
new_age1 = int(input("Enter a new age - "))  # Example: 40
second_user = User(new_name1, new_age1)
print(second_user)  # Output: User's name - Bob, user's age - 40
           