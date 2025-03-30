from os import sync
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
from pathlib import Path


def count_holes(region):
    shape = region.image.shape
    new_image = np.zeros((shape[0] + 2, shape[1] + 2))
    new_image[1:-1, 1:-1] = region.image
    new_image = np.logical_not(new_image)
    labeled = label(new_image)
    return np.max(labeled) - 1


def count_vlines(region):
    return np.all(region.image, axis=0).sum()


def count_lgr_vlines(region):
    x = region.image.mean(axis=0) == 1
    return np.sum(x[: len(x) // 2]) and np.sum(x[len(x) // 2 :])


def recognize(region):
    if np.all(region.image):
        return "-"
    else:
        holes = count_holes(region)
        if holes == 2:  # 8 or B
            # vlines = count_vlines(region)
            _, cx = region.centroid_local
            cx /= region.image.shape[1]
            if cx < 0.44:
                return "B"
            return "8"
        elif holes == 1:  # A, 0
            pass
        else:
            pass
    return "#"


image = plt.imread(Path(__file__).parent / "alphabet.png")[:, :, :-1]
gray = image.mean(axis=2)
binary = gray > 0
labeled = label(binary)
regions = regionprops(labeled)


out_path = Path(__file__).parent / "out"
out_path.mkdir(exist_ok=True)
result = {}

plt.figure()

for i, region in enumerate(regions):
    print(f"{i + 1}/{len(regions)}")
    symbol = recognize(region)
    if symbol not in result:
        result[symbol] = 0
    result[symbol] += 1
    plt.cla()
    plt.title(symbol)
    plt.imshow(region.image)
    plt.savefig(out_path / f"{i:03d}.png")

print(result)
