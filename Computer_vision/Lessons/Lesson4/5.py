import numpy as np
import matplotlib.pyplot as plt
from scipy.datasets import face


def block_mean(image, ybc, xbc):
    result = image.copy()
    ybs = image.shape[0] // ybc
    xbs = image.shape[1] // xbc
    for y in range(0, image.shape[0], ybs):
        for x in range(0, image.shape[1], xbs):
            sub = image[y : y + ybs, x : x + xbs]
            result[y : y + ybs, x : x + xbs] = sub.mean()
    return result


image = face(gray=True)

plt.imshow(block_mean(image, 100, 100))
plt.show()
