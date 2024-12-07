from datetime import datetime
from functools import singledispatchmethod

class BirthInfo:
    @singledispatchmethod
    def __init__(self, birth_date):
        raise TypeError("The passed type argument is not supported")

    @__init__.register(str)
    def from_str(self, birth_date):
        year, month, day = map(int, birth_date.split("-"))
        self.birth_date = datetime(year, month, day)

    @__init__.register(tuple)
    def from_tuple(self, birth_date):
        year, month, day = birth_date
        self.birth_date = datetime(year, month, day)

    @__init__.register(list)
    def from_list(self, birth_date):
        year, month, day = birth_date
        self.birth_date = datetime(year, month, day)

    @__init__.register(datetime)
    def from_datetime(self, birth_date):
        self.birth_date = birth_date

    def current_age(self):
        now = datetime.now()
        age = now.year - self.birth_date.year
        if (now.month, now.day) < (self.birth_date.month, self.birth_date.day):
            age -= 1
        return age

    def __str__(self):
        return (f"Birth Date: {self.birth_date.strftime('%Y-%m-%d')}\n"
                f"Current Age: {self.current_age()}")

# Examples
birthday1 = BirthInfo("2020-12-10")
print(birthday1)

birthday2 = BirthInfo((2006, 9, 25))
print(birthday2)

birthday3 = BirthInfo([2000, 9, 11])
print(birthday3)

# For example
# birthday4 = BirthInfo(123)
# print(birthday4)