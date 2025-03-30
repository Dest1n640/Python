import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import regionprops, label


def extractor(region):
    area = region.area / region.image.size
    return np.array([area])


def norm_l1(v1, v2):
    return ((v1 - v2) ** 2).sum() ** 0.5


def classificator(v, templates):
    result = "_"
    min_dist = 10**16
    for key in templates:
        d = norm_l1(v, templates[key])
        if d < min_dist:
            result = key
            min_dist = d
    return result


image = plt.imread("alphabet.png")[:, :, :-1]
gray = image.mean(axis=2)
binary = gray > 0
labeled = label(binary)
regions = regionprops(labeled)
print(len(regions))


symbols = plt.imread("./alphabet-small.png")[:, :, :-1]
sgray = symbols.mean(axis=2)
sbinary = sgray < 1
slabeled = label(sbinary)
sregions = regionprops(slabeled)
print(len(sregions))


plt.subplot(121)
plt.imshow(symbols)
plt.subplot(122)
plt.imshow(image)
plt.show()
