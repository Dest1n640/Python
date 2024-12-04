import math

class Figure:
    def volume(self):
        raise NotImplementedError("This method should be overridden in derived classes")

    def surface_area(self):
        raise NotImplementedError("This method should be overridden in derived classes")

class Cube(Figure):
    def __init__(self, side):
        if side < 0:
            raise ValueError("Side length cannot be negative")
        self.side = side

    def volume(self):
        return self.side ** 3

    def surface_area(self):
        return 6 * (self.side ** 2)

    def __str__(self):
        return f"Cube(side={self.side})"


class Sphere(Figure):
    def __init__(self, radius):
        if radius < 0:
            raise ValueError("Radius cannot be negative")
        self.radius = radius

    def volume(self):
        return (4 / 3) * math.pi * (self.radius ** 3)

    def surface_area(self):
        return 4 * math.pi * (self.radius ** 2)

    def __str__(self):
        return f"Sphere(radius={self.radius})"


class Cylinder(Figure):
    def __init__(self, radius, height):
        if radius < 0 or height < 0:
            raise ValueError("Radius and height cannot be negative")
        self.radius = radius
        self.height = height

    def volume(self):
        return math.pi * (self.radius ** 2) * self.height

    def surface_area(self):
        return 2 * math.pi * self.radius * (self.radius + self.height)

    def __str__(self):
        return f"Cylinder(radius={self.radius}, height={self.height})"


class Parallelepiped(Figure):
    def __init__(self, length, width, height):
        if length < 0 or width < 0 or height < 0:
            raise ValueError("Dimensions cannot be negative")
        self.length = length
        self.width = width
        self.height = height

    def volume(self):
        return self.length * self.width * self.height

    def surface_area(self):
        return 2 * (self.length * self.width + self.width * self.height + self.height * self.length)

    def __str__(self):
        return f"Parallelepiped(length={self.length}, width={self.width}, height={self.height})"


class Ellipsoid(Figure):
    def __init__(self, axis_a, axis_b, axis_c):
        if axis_a < 0 or axis_b < 0 or axis_c < 0:
            raise ValueError("Axes lengths cannot be negative")
        self.axis_a = axis_a
        self.axis_b = axis_b
        self.axis_c = axis_c

    def volume(self):
        return (4 / 3) * math.pi * self.axis_a * self.axis_b * self.axis_c

    def surface_area(self):
        # Approximation of surface area
        p = 1.6075
        return 4 * math.pi * (
            ((self.axis_a ** p) * (self.axis_b ** p) +
             (self.axis_a ** p) * (self.axis_c ** p) +
             (self.axis_b ** p) * (self.axis_c ** p)) / 3
        ) ** (1 / p)

    def __str__(self):
        return f"Ellipsoid(axis_a={self.axis_a}, axis_b={self.axis_b}, axis_c={self.axis_c})"


def find_dominant_figure(figures):
    total_volume = sum(fig.volume() for fig in figures)
    dominant_figures = [fig for fig in figures if fig.volume() >= total_volume - fig.volume()]
    return dominant_figures


# Example usage:
figures = [
Cube(3),Sphere(2),Cylinder(2, 5),Parallelepiped(2, 3, 4), Ellipsoid(2, 3, 4)]

dominant_figures = find_dominant_figure(figures)
for fig in figures:
    print(f"{fig}: Volume={fig.volume():.2f}, Surface Area={fig.surface_area():.2f}")

print("\nDominant Figures:")
for fig in dominant_figures:
    print(f"{fig}: Volume={fig.volume():.2f}")
