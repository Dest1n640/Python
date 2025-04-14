import numpy as np
import matplotlib.pyplot as plt

image = np.zeros((100, 100))

image[::2, ::2] = 1
image[1::2, 1::2] = 1

plt.imshow(image)
plt.show()
