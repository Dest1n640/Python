import numpy as np
import matplotlib.pyplot as plt

image = np.ones((600, 600))
d = 250

y = np.arange(600).reshape(600, 1) - 300
x = np.arange(600).reshape(1, 600) - 300

mask = x**2 + y**2 < (d / 2) ** 2

plt.imshow(mask)
plt.show()
