import math
from abc import ABC, abstractmethod


class Figure3D(ABC):
    @abstractmethod
    def get_volume(self):
        pass

    @abstractmethod
    def get_surface_area(self):
        pass

    @abstractmethod
    def __str__(self):
        pass


class Cube(Figure3D):
    def __init__(self, a):
        self.a = a

    def get_volume(self):
        return self.a ** 3

    def get_surface_area(self):
        return 6 * (self.a ** 2)

    def __str__(self):
        return f"Cube: S = {self.get_surface_area()}; V = {self.get_volume()}"


class Sphere(Figure3D):
    def __init__(self, r):
        self.r = r

    def get_volume(self):
        return (4 / 3) * math.pi * (self.r ** 3)

    def get_surface_area(self):
        return 4 * math.pi * (self.r ** 2)

    def __str__(self):
        return f"Sphere: S = {self.get_surface_area()}; V = {self.get_volume()}"


class Cylinder(Figure3D):
    def __init__(self, r, h):
        self.r = r
        self.h = h

    def get_volume(self):
        return math.pi * (self.r ** 2) * self.h

    def get_surface_area(self):
        return 2 * math.pi * self.r * (self.r + self.h)

    def __str__(self):
        return f"Cylinder: S = {self.get_surface_area()}; V = {self.get_volume()}"


class Parallelepiped(Figure3D):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def get_volume(self):
        return self.a * self.b * self.c

    def get_surface_area(self):
        return 2 * (self.a * self.b + self.b * self.c + self.a * self.c)

    def __str__(self):
        return f"Parallelepiped: S = {self.get_surface_area()}; V = {self.get_volume()}"


class Ellipsoid(Figure3D):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def get_volume(self):
        return (4 / 3) * math.pi * self.a * self.b * self.c

    def get_surface_area(self):
        p = 1.6075
        return (4* math.pi* (((self.a * self.b) ** p+ (self.b * self.c) ** p+ (self.a * self.c) ** p)/ 3) ** (1 / p))

    def __str__(self):
        return f"Ellipsoid: S = {self.get_surface_area()}; V = {self.get_volume()}"


def find_large_volume_figures(figures):
    total_volume = sum(figure.get_volume() for figure in figures)
    large_figures = [figure for figure in figures if figure.get_volume() >= total_volume - figure.get_volume()]

    if large_figures:
        print("Figures with volume equal to or greater than the sum of the volumes of other figures:")
        for fig in large_figures:
            print(fig)
    else:
        print("No figure has a volume greater than or equal to the sum of the other figures.")


# Example Usage
shapes = [
    Cube(3),
    Sphere(4),
    Cylinder(2, 5),
    Parallelepiped(2, 3, 4),
    Ellipsoid(3, 2, 1)
]

for shape in shapes:
    print(shape)

print("\nChecking for large volume figures...")
find_large_volume_figures(shapes)
