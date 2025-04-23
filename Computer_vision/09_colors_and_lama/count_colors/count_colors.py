import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
import numpy as np
from skimage.morphology import (
    binary_closing,
    binary_dilation,
    binary_erosion,
    binary_opening,
)
from skimage.color import rgb2hsv

image = plt.imread("./balls.png")
hsv_image = rgb2hsv(image)
gray = image.mean(axis=2)
binary = gray > 0

binary = binary_erosion(binary, np.ones((3, 3)))

labeled = label(binary)
regions = regionprops(labeled)

count = 0
colors = []
for region in regions:
    if region.eccentricity == 0.0:
        y, x = region.centroid
        colors.append(hsv_image[int(y), int(x), 0])
        count += 1
    else:
        coords = region.coords
        region_colors = hsv_image[coords[:, 0], coords[:, 1], 0]
        unique_colors = np.unique(region_colors, axis=0)
        colors.extend(unique_colors)
        count += 2

print(count)
print(len(colors))

d = np.diff(sorted(colors))
pos = np.where(d > np.std(d) * 2)
print(len(pos[0]) + 1)

plt.subplot(121)
plt.imshow(hsv_image)
plt.subplot(122)
plt.plot(sorted(colors), "o-")
plt.show()
