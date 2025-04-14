from math import sqrt

points_list = [[1, 1], [4, 5], [7, 1], [-1, 3], [4, 4]]


def distance(points):
    max_distance = 0
    point1_max = None
    point2_max = None
    for i in range(len(points) - 1):
        for j in range(i + 1, len(points)):
            point1 = points[i]
            point2 = points[j]

            distance_value = sqrt(
                (point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2
            )

            if distance_value > max_distance:
                max_distance = distance_value
                point1_max = point1
                point2_max = point2

    return point1_max, point2_max, max_distance


point1, point2, max_dist = distance(points_list)


def circle(r, point_x, point_y, centre_x, centre_y):
    distance_from_point = (point_x - centre_x) ** 2 - (point_y - centre_y) ** 2
    r = r**2
    return distance_from_point <= r


# points
print(f"Точка 1 = {point1}")
print(f"Точка 2 = {point2}")
print(f"Макс элемент = {max_dist}")


# circle
print(circle(10, 5, 5, 10, 10))
