import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import binary_erosion
from skimage.measure import label
from skimage.morphology import binary_closing, binary_opening, binary_dilation


data = np.loadtxt("files/wires2npy.txt")

labeled = label(data)
print(np.max(labeled))

result = binary_erosion(data, np.ones(3).reshape(3, 1))

plt.imshow(result)
plt.show()
plt.imshow(data)
plt.show()
