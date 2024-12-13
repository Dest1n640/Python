class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return f"({self.x};{self.y})"
    def __repr__(self):
        return f"({self.x};{self.y})"
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __hash__(self):
        return id(self)//(self.x + self.y)

p1 = Point(2, 3)
p2 = Point(2, 3)
print(p1)
print(p2)
print(p1 == p2)
print(id(p1))
print(id(p2))
print(hash(p1))
print(hash(p2))
print(id(p1) == id(p2))
print(hash(p1) == hash(p2))
d = {}
d[p1] = "First"
print(d)