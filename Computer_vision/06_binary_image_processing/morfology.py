import numpy as np
import matplotlib.pyplot as plt


def dilation(arr):
    result = np.zeros_like(arr)
    for y in range(1, arr.shape[0] - 1):
        for x in range(1, arr.shape[1] - 1):
            sub = np.logical_and(arr[y, x], struct)
            result[y - 1 : y + 2, x - 1 : x + 2] = np.logical_or(
                result[y - 1 : y + 2, x - 1 : x + 2], sub
            )
    return result


def erosion(arr):
    result = np.zeros_like(arr)
    for y in range(1, arr.shape[0] - 1):
        for x in range(1, arr.shape[1] - 1):
            sub = arr[y - 1 : y + 2, x - 1 : x + 2]
            if np.all(sub == struct):
                result[y, x] = 1
    return result


def closing(arr):
    return erosion(dilation(arr))


def opening(arr):
    return dilation(erosion(arr))


arr = np.array(
    [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
)

struct = np.ones((3, 3))
plt.subplot(151)
plt.imshow(arr)
plt.title("Original")

plt.subplot(152)
plt.imshow(dilation(arr))
plt.title("Dilation")

plt.subplot(153)
plt.imshow(erosion(arr))
plt.title("Erosion")

plt.subplot(154)
plt.imshow(closing(arr))
plt.title("Closing")

plt.subplot(155)
plt.imshow(opening(arr))
plt.title("Opening")
plt.show()
