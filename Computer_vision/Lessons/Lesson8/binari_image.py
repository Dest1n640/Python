import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import binary_closing
from skimage import draw


def hist(arr):
    h = np.zeros(256)
    for v in arr.flatten():
        h[v] += 1
    return h


image = np.zeros((500, 500), dtype="uint8")
image[:] = np.random.randint(0, 50, image.size).reshape(image.shape)

rr, cc = draw.disk((150, 150), 75)
image[rr, cc] = np.random.randint(40, 80, len(rr))

rr, cc = draw.disk((350, 350), 75)
image[rr, cc] = np.random.randint(70, 120, len(rr))

plt.figure()
plt.subplot(121)
plt.imshow(image)
plt.subplot(122)
plt.plot(hist(image))

plt.figure()
binary = image.copy()
binary[binary < 60] = 0
binary[binary > 0] = 1
binary = binary_closing(binary, np.ones((10, 10)))
plt.imshow(binary)
plt.show()
