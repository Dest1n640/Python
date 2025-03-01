import numpy as np
import matplotlib.pyplot as plt

external = np.array(
    [[[0, 0], [0, 1]], [[0, 0], [1, 0]], [[0, 1], [0, 0]], [[1, 0], [0, 0]]]
)
internal = np.logical_not(external)
external_fix = np.array([[[1, 0], [0, 1]], [[0, 1], [1, 0]]])


def match(sub, masks):
    for i in masks:
        if np.all(sub == i):
            return True
    return False


def count_objects(image):
    E = 0
    for y in range(0, image.shape[0] - 1):
        for x in range(0, image.shape[1] - 1):
            sub = image[y : y + 2, x : x + 2]
            if match(sub, external):
                E += 1
            elif match(sub, internal):
                E -= 1
            elif match(sub, external_fix):
                E += 2
    return E / 4


path = "cex2npy.txt"
image = np.load(path)
print(image.shape)

print(sum([count_objects(image[:, :, i]) for i in range(image.shape[2])]))

plt.imshow(image)
plt.show()
