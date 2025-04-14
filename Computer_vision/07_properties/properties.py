import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import label


def area(labeled, lbl):
    return (labeled == lbl).sum()


def centroid(labeled, lbl):
    pos_y, pos_x = np.where(labeled == lbl)
    cy = pos_y.mean()
    cx = pos_x.mean()
    return cy, cx


def neighbours4(y, x):
    return (y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)


def neighbourX(y, x):
    return (y - 1, x + 1), (y + 1, x + 1), (y + 1, x - 1), (y - 1, x - 1)


def neighbours8(y, x):
    return neighbourX(y, x) + neighbours4(y, x)


def boundaries(labeled, lbl, connectivity=neighbours8):
    pos = np.where(labeled == lbl)
    bounds = []
    for y, x in zip(*pos):
        for yn, xn in connectivity(y, x):
            if yn < 0 or yn > labeled.shape[0] - 1:
                bounds.append((y, x))
                break
            elif xn < 0 or xn > labeled.shape[1] - 1:
                bounds.append((y, x))
                break
            elif labeled[yn, xn] == 0:
                bounds.append((y, x))
                break
    return bounds


def draw_bounds(labeled, connectivity=neighbours8):
    result = labeled.copy()
    for i in range(1, labeled.max() + 1):
        bounds = boundaries(labeled, i, connectivity)
        for y, x in bounds:
            result[y, x] += 1
    return result


def perimenter(labeled, lbl, connectivity=neighbours8):
    return len(boundaries(labeled, lbl, connectivity))


def circularity(labeled, lbl, connectivity=neighbours8):
    return perimenter(labeled, lbl, connectivity) ** 2 / area(labeled, lbl)


def distance(px1, px2):
    return ((px1[0] - px2[0]) ** 2 + (px1[1] - px2[1]) ** 2) ** 0.5


def radial_distance(labeled, lbl, connectivity=neighbours8):
    r, c = centroid(labeled, lbl)
    bounds = boundaries(labeled, lbl, connectivity)
    K = len(bounds)
    rd = 0
    for rk, ck in bounds:
        rd += distance((r, c), (rk, ck))
    return rd / K


def std_radual(labeled, lbl, connectivity=neighbours8):
    r, c = centroid(labeled, lbl)
    bounds = boundaries(labeled, lbl, connectivity)
    K = len(bounds)
    sr = 0
    rd = radial_distance(labeled, lbl, connectivity)
    for rk, ck in bounds:
        sr += (distance((r, c), (rk, ck)) - rd) ** 2
    return (sr / K) ** 0.5


def circularity_std(labeled, lbl, connectivity=neighbours8):
    return radial_distance(labeled, lbl, connectivity) / std_radual(
        labeled, lbl, connectivity
    )


LB = np.zeros((16, 16), dtype="int")
LB[4:, :4] = 2

LB[3:10, 8:] = 1
LB[[3, 4, 3], [8, 8, 9]] = 0
LB[[8, 9, 9], [8, 8, 9]] = 0
LB[[3, 4, 3], [-2, -1, -1]] = 0
LB[[9, 8, 9], [-2, -1, -1]] = 0

LB[12:-1, 6:9] = 3

for i in range(1, np.max(LB + 1)):
    # print(area(LB, i))
    # cy, cx = centroid(LB, i)
    # print(cx, cy)
    # plt.scatter([cx], [cy])
    # print(perimenter(LB, i))
    # print(perimenter(LB, i, neighbours4))
    # print(is_circl(LB, i))
    # print(is_circl(LB, i, neighbours4))
    print(circularity_std(LB, i))
    print(circularity_std(LB, i, neighbours4))
    ...

plt.imshow(draw_bounds(LB))
plt.show()
