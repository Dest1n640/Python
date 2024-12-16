from abc import ABC, abstractclassmethod
class Figur:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    @abstractclassmethod
    def area(self):
        pass
    @abstractclassmethod
    def perimeter(self):
        pass
class Circle(Figur):
    def __init__(self, x, y, r):
        Figur.__init__(self, x, y)
        self.r = r
        
fig = Figur(2,5)
circl = Circle(1,1,6)
print(fig.area())
print(circl.area())