import numpy as np
from numpy import ndarray
from tqdm import tqdm


def gradient(pixels: ndarray, operator_gx: ndarray, operator_gy: ndarray) -> (ndarray, ndarray, ndarray, ndarray):
    height = pixels.shape[0]
    width = pixels.shape[1]

    b = operator_gy.shape[0]

    gx = np.zeros(shape=(height, width), dtype=np.int8)
    gy = np.zeros(shape=(height, width), dtype=np.int8)
    g = np.zeros(shape=(height, width), dtype=np.int8)
    delta = int(b / 2)
    for x in tqdm(range(delta, width - delta - 1), ascii=True, desc="gradient"):
        for y in range(delta, height - delta - 1):
            local_window = pixels[y - delta:y + delta + 1, x - delta:x + delta + 1, 0]
            gx[y, x] = np.sum(local_window * operator_gx)
            gy[y, x] = np.sum(local_window * operator_gy)
    # gx += np.min(gx)
    gx = gx / np.max(gx) * 255
    # gy += np.min(gy)
    gy = gy / np.max(gy) * 255
    g = np.absolute(gx) + np.absolute(gy)

    g = g * (255 / np.max(g))
    new_image = np.copy(g)
    new_image[new_image >= np.max(new_image) / 2] = 225
    new_image[new_image < np.max(new_image) / 2] = 0
    return gx, gy, g, new_image
