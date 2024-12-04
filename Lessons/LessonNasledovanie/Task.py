import random
class Point:
    def __init__(self, x, y):
        self.__x = x # Приватные элементы не наследуются но можно использовать сеттеры и геттеры
        self.__y = y
    def move(self, dx1, dy1):
        self.__x += dx1
        self.__y += dy1
    def get_x(self):
        return self.__x
    def get_y(self):
        return self.__y
    def __str__(self):
        return f"{self.get_x()};{self.get_y()}"
class Circle(Point):
    def __init__(self, x,y, r = 1):
        Point.__init__(self, x, y)
        self.r = r
    
    def __str__(self):
        return f"{self.get_x()};{self.get_y()}"
c1 = Point(3, 6)
print(c1)
c1.move(1,2)
print(c1)
my_list = []
for i in range(8+1):
    rand = random.randint(1, 100)
    if rand > 50:
        my_list.append(Circle(random.randint(1,50), random.randint(1,50)))
    else:
        my_list.append(Point(random.randint(1,50), random.randint(1,50)))
for fig in my_list:
    print(fig)