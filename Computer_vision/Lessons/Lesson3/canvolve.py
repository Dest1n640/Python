from re import sub
import matplotlib.pyplot as plt
import numpy as np
from scipy.datasets import face

image = face(gray=True)


def convolve(image: np.ndarray, mask: np.ndarray) -> np.ndarray:
    result: np.ndarray = np.zeros(image.shape)
    for i in range(1, image.shape[0] - 1):
        for j in range(1, image.shape[1] - 1):
            sub_image = image[i - 1 : i + 2, j - 1 : j + 2]
            value: int = np.sum(sub_image * mask)
            result[i, j] = value
    return result[1:-1, 1:-1]


second = [[-1, 2, -1], [-1, 2, -1], [-1, 2, -1]]
third_arr = [[-1, -1, 2], [-1, 2, -1], [2, -1, -1]]
forth_arr = [[2, -1, -1], [-1, 2, -1], [-1, -1, 2]]
mask_1 = np.array(third_arr)
result_1 = convolve(image, mask_1)
plt.subplot(121)
plt.imshow(result_1)
plt.clim(0, 100)
mask_2 = np.array(third_arr)
result_2 = convolve(image, mask_2)
plt.subplot(122)
plt.imshow(result_2)
plt.clim(0, 100)
plt.show()
