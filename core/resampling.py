from PIL import Image, ImageDraw
import numpy as np


def resampling(image: Image.Image, n: float, method: str = "nearest_neighbor") -> Image.Image:
    """
    Используется метод ближайшего соседа
    """

    width = image.size[0]
    height = image.size[1]
    pix = np.array(image)

    new_width = round(width * n)
    new_height = round(height * n)

    if method == "nearest_neighbor":
        new_image = nearest_neighbor(pix, width, height, new_width, new_height)
    elif method == "cubic":
        new_image = cubic(pix, new_width, new_height)

    new_image = Image.fromarray(new_image.astype(np.uint8)).convert("RGB")
    return new_image


def nearest_neighbor(pix, width, height, new_width, new_height) -> np.ndarray:
    new_image = np.zeros((new_height, new_width, 3))

    for x in range(new_width):
        for y in range(new_height):
            src_x = min(
                int(round(float(x) / float(new_width) * float(width))),
                width - 1)
            src_y = min(
                int(round(float(y) / float(new_height) * float(height))),
                height - 1)

            new_image[y, x] = pix[src_y, src_x]

    return new_image


def cubic(pix, new_width, new_height) -> np.ndarray:
    new_image = np.zeros((new_height, new_width, 3))

    for x in range(new_width):
        for y in range(new_height):

            x_1 = np.floor(x).astype(int)
            x_2 = x + 1
            y_1 = np.floor(y).astype(int)
            y_2 = y + 1

            w_a = (x_2 - x) * (y_2 - y)
            w_b = (x - x_1) * (y_2 - y)
            w_c = (x_2 - x) * (y - y_1)
            w_d = (x - x_1) * (y - y_1)

            d = (x_2 - x_1) * (y_2 - y_1)

            new_image[y, x] = (pix[y_1, x_1] / d) * w_a +\
                              (pix[y_2, x_1] / d) * w_b +\
                              (pix[y_1, x_2] / d) * w_c +\
                              (pix[y_2, x_2] / d) * w_d

    return new_image