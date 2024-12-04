class NDrob:
    def __init__(self, num=1, denom=1):
        self.num = num
        if denom != 0:
            self.denom = denom
        else:
            raise ValueError("ERROR")
    
    def __str__(self):
        return str(self.num) + "/" + str(self.denom)
    
    def multy(self, other):
        if isinstance(other, NDrob):
            res = NDrob()
            res.num = self.num * other.num
            res.denom = self.denom * other.denom
            return res
        else:
            return NotImplemented

class IncorrDrob(NDrob):
    def __init__(self, num, denom):
        if num >= denom and denom != 0:
            self.part = num // denom
            super().__init__(num % denom, denom)
        else:
            raise ValueError("Invalid input: num must be >= denom and denom must not be 0")
    
    def __str__(self):
        return f"Дробь равна - {self.part} целых {self.num} / {self.denom}"
    
    def multy(self, otherIr):
        if isinstance(otherIr, IncorrDrob):
            self.num += self.part * self.denom
            otherIr.num += otherIr.part * otherIr.denom
            res = super().multy(otherIr)
            return IncorrDrob(res.num, res.denom)
        else:
            return NotImplemented

inc = IncorrDrob(40, 23)
print(inc)
