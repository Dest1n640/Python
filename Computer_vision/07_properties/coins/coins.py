import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label
from collections import defaultdict


def area(labeled, lbl):
    return (labeled == lbl).sum()


image = np.load("./coins.npy")

labeled = label(image)
print(area(labeled, 6))

areas = defaultdict(lambda: 0)
for lbl in range(1, np.max(labeled) + 1):
    areas[area(labeled, lbl)] += 1

print(areas)
nominals = np.array([1, 2, 5, 10], dtype=int)
meaning = 0

sorted_areas = np.array(sorted(areas.items()))
answer = nominals * sorted_areas[:, 1]

# for i in range(len(nominals)):
#    fig = sorted(areas.keys())
#    meaning += nominals[i] * areas.get(fig[i])
#    print(meaning)

print(sum(answer))

plt.imshow(image)
plt.show()
