class ColoredPoint:
    def  __init__(self, x, y, color):
        if isinstance(x, int) and isinstance(y, int) and isinstance(color, str):
            self.x = x
            self.y = y
            self.color = color
        else: raise NotImplemented()
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def get_color(self):
        return self.color
    def __eq__(self, other):
        return f"Equal = {self.x == other.x and self.y == other.y and self.color == other.color}"
    def __str__(self):
        return f"{self.x}, {self.y}, {self.color}"
    def __hash__(self):
        return hash((self.x, self.y, self.color))
    def __repr__(self):
        return f"{self.x}, {self.y}, {self.color}"

p1 = ColoredPoint(1, 2, "red")
p2 = ColoredPoint(1, 2, "red")
p3 = ColoredPoint(3, 4, "blue")

print(p1.x)
print(p1.y)
print(p1.color)

print(repr(p1))

print(p1 == p2)
print(p1 == p3)

points_dict = {p1: "Point 1", p3: "Point 3"}
print(points_dict[p1])
print(points_dict[p3])