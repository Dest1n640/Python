import math

class VectorLong:
    def __init__(self, x1, y1):
        self.x1 = x1
        self.y1 = y1

    def length(self):
        return math.sqrt(self.x1**2 + self.y1**2)

    def tilt(self):
        if self.x1== 0 and self.y1 == 0:
            return "Точки совпадают, угол не определён."
        elif self.x1 == 0:
            return 90.0 if y2 > self.y1 else -90.0
        else:
            angle_rad = math.atan2(self.y1, self.x1)
            return math.degrees(angle_rad)

    def sum(self, x2, y2):
        return (self.x1 + x2, self.y1 + y2)

    def minus(self, x2, y2):
        return (self.x1 - x2, self.y1 - y2)

    def muilt(self, x2, y2):
        return (self.x1 * x2 + self.y1 * y2)

x1, y1, x2, y2 = map(float, input("Введите значения (x1, y1, x2, y2): ").split())

vector = VectorLong(x1,y1)

print("Длина вектора:", vector.length())
print("Угол наклона вектора к оси x:", vector.tilt(), "градусов")
print("Сумма векторов:", vector.sum(x2, y2))
print("Разность векторов:", vector.minus(x2, y2))
print("Скалярное произведение векторов:", vector.muilt(x2, y2))