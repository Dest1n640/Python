import numpy as np
import matplotlib.pyplot as plt
from scipy.datasets import face


def mse(reference, noised):
    return ((reference - noised) ** 2).sum() / reference.size


def psnr(reference, noised):
    return 20 * np.log10(reference.max() / np.sqrt(mse(reference, noised)))


image = face(gray=True)
noised = image.copy()

noise_percent = 10
noised_pixels = int(noise_percent * image.size)

y_pos, x_pos = np.meshgrid(np.arange(image.shape[0]), np.arange(image.shape[1]))
y_pos = y_pos.flatten()
x_pos = x_pos.flatten()
pos = np.random.choice(np.arange(len(y_pos)), noised_pixels)
yn = y_pos[pos]
xn = x_pos[pos]
noised[yn, xn] = np.random.randint(0, 255, noised_pixels)

print(psnr(image, noised))

plt.figure()
plt.subplot(121)
plt.title("Original")
plt.imshow(image)
plt.subplot(122)
plt.title("Noised")
plt.imshow(noised)
plt.show()
