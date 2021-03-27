import numpy as np
from PIL.Image import Image
from numpy import ndarray
from tqdm import tqdm


def gradient(image: Image, operator_gx: ndarray, operator_gy: ndarray) -> (ndarray, ndarray, ndarray, ndarray):
    pixels = np.array(image)
    height = pixels.shape[0]
    width = pixels.shape[1]

    b = operator_gy.shape[0]  # Размер окна

    gx = np.zeros(shape=(height, width))  # Двумерные массивы под частные производные
    gy = np.zeros(shape=(height, width))
    g = np.zeros(shape=(height, width))
    gnormalx = np.zeros(shape=(height, width))
    gnormaly = np.zeros(shape=(height, width))
    gnormal = np.zeros(shape=(height, width))

    delta = int(b / 2)
    if image.mode == "L":
        for x in tqdm(range(delta, width - delta), ascii=True, desc="gradient"):
            for y in range(delta, height - delta):
                local_window = pixels[y - delta:y + delta + 1, x - delta:x + delta + 1]
                gx[y, x] = np.sum(local_window * operator_gx)
                gy[y, x] = np.sum(local_window * operator_gy)
    else:
        for x in tqdm(range(delta, width - delta), ascii=True, desc="gradient"):
            for y in range(delta, height - delta):
                local_window = pixels[y - delta:y + delta + 1, x - delta:x + delta + 1, 0]
                gx[y, x] = np.sum(local_window * operator_gx)
                gy[y, x] = np.sum(local_window * operator_gy)

    Min = gx.min()
    Max = gx.max()
    gnormalx = (gx - Min)*(255/(Max-Min))

    Min = gy.min()
    Max = gy.max()
    gnormaly = (gy - Min)*(255/(Max-Min))

    for x in range(len(gx[0])):
        for y in range(len(gy)):
            g[y, x] = abs(gnormalx[y, x]) + abs(gnormaly[y, x])

    Min = g.min()
    Max = g.max()
    gnormal = (g - Min)*(255/(Max-Min))

    return gnormalx, gnormaly, gnormal