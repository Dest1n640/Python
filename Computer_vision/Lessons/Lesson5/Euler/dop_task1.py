import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label

masks = np.array([[[0, 0], [0, 1]], [[0, 1], [1, 1]]])


def match(sub, mask):
    if np.all(sub == mask):
        return True
    return False


def euler_number(image):
    m1 = 0
    m2 = 0
    for y in range(0, image.shape[0] - 1):
        for x in range(0, image.shape[1] - 1):
            sub = image[y : y + 2, x : x + 2]
            if match(sub, masks[0]):
                m1 += 1
            elif match(sub, masks[1]):
                m2 += 1

    return m1 - m2


image = np.load("holes.npy")
labeled = label(image)
for lbl in range(1, labeled.max() + 1):
    fig = labeled == lbl
    plt.subplot(3, 3, lbl)
    plt.title(f"Holes = {euler_number(fig)}")
    plt.imshow(fig)

plt.show()
