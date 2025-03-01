import numpy as np
import matplotlib.pyplot as plt
from scipy.datasets import face


def descritize(image, level):
    mn = image.min()
    mx = np.max(image)
    result = image.copy()
    percent = (result - mn) / (mx - mn)
    result = (percent * level).astype("uint64")
    return result


image = face(gray=True)

plt.imshow(descritize(image, 32000))
plt.show()

plt.imshow(image)
plt.show()
