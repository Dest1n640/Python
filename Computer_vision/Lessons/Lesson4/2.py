import numpy as np
import matplotlib.pyplot as plt

image = np.zeros((500, 500))
bs = 25
count = 0
for y in range(0, image.shape[0], bs):
    for x in range(0, image.shape[1], bs):
        image[y : y + bs, x : x + bs] = count
        count += 1


plt.imshow(image)
plt.show()
