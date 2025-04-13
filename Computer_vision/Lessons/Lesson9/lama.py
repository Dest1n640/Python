import matplotlib.pyplot as plt
import numpy as np
from skimage.filters import sobel, threshold_otsu
from skimage.measure import label, regionprops
from scipy.ndimage import binary_fill_holes


def flood_fill(mask, y, x):
    filled = np.zeros_like(mask, dtype=bool)
    h, w = mask.shape
    stack = [(y, x)]

    while stack:
        cy, cx = stack.pop()

        if cy < 0 or cy >= h or cx < 0 or cx >= w:
            continue
        if mask[cy, cx] or filled[cy, cx]:
            continue

        filled[cy, cx] = True

        stack.append((cy + 1, cx))
        stack.append((cy - 1, cx))
        stack.append((cy, cx + 1))
        stack.append((cy, cx - 1))

    return ~filled


image = plt.imread("lama-on-moon.png")[50:-50, 50:-50, :-1]

image = image.mean(axis=2)
s = sobel(image)

thesh = threshold_otsu(s)
print(thesh)

s[s < thesh] = 0
s[s >= thesh] = 1

labeled = label(s)
regions = regionprops(labeled)
regions = sorted(regions, key=lambda item: item.perimeter)

result = np.logical_or(labeled == regions[-1].label, labeled == regions[-2].label)

min_row, min_col, max_row, max_col = regions[-1].bbox
for region in regions[:-2]:
    if region.perimeter < 50:
        continue
    cy, cx = region.centroid
    if min_row < cy < max_row and min_col < cx < max_col:
        result = np.logical_or(result, labeled == region.label)

# lama_filled = binary_fill_holes(result)

outside_y, outside_x = 0, 0
outside_filled = flood_fill(result, outside_y, outside_x)

lama_filled = outside_filled


plt.subplot(1, 3, 1)
plt.imshow(image)

plt.subplot(1, 3, 2)
plt.imshow(result)

plt.subplot(1, 3, 3)
plt.imshow(lama_filled)
plt.show()
