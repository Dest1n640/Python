class USADate:
    month30 = [4, 6, 9, 11]
    def __init__(self, year, month, day):
        if isinstance(year, int) and isinstance(month, int) and isinstance(day, int):
            if 1 <= month <= 12 and 0 <= year and 1 <= day <= 31:
                for i in self.month30:
                    if i == month:
                        if day == 31:
                            raise ValueError("The incorrect date")
                        else:
                            self.day = day
                            self.year = year
                            self.month = month
                    elif i == 2:
                        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                            if day <= 29:
                                self.day = day
                                self.year = year
                                self.month = month
                            else:
                                raise ValueError("Incorrect date")
                        else:
                            if day <= 28:
                                self.day = day
                                self.year = year
                                self.month = month
                            else:
                                raise ValueError("Incorrect date")
            else:
                raise ValueError("The date is incorrect")
        else:
            raise ValueError("The date must be int")

    def format(self):
        return f"{self.month}-{self.day}-{self.year}"
    def iso_format(self):
        return f"{self.year}-{self.month}-{self.day}"

class ItalianDate(USADate):
    def __init__(self, year, month, day):
        USADate.__init__(self, year, month, day)

    def format(self):
        return f"{self.day}/{self.month}/{self.year}"
    def iso_format(self):
        return f"{self.year}-{self.month}-{self.day}"

date = [int(i) for i in input("Input the data in the format(year.month.day): ").split(".")]
data1 = USADate(*date)
data2 = ItalianDate(*date)
