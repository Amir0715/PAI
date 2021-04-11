import numpy as np
from PIL import Image
from PIL import ImageDraw


def halftone(image: Image.Image, r=1 / 3, g=1 / 3, b=1 / 3) -> Image.Image:
    if image.mode == "L":
        return image
    pix = np.array(image)
    new_image = (r * pix[:, :, 0] + g * pix[:, :, 1] + b * pix[:, :, 2])
    return Image.fromarray(new_image.astype(np.uint8)).convert("RGB")


def sepia(image: Image.Image, k: int) -> Image.Image:
    pix = image.load()  # Выгружаем значения пикселей.
    width = image.size[0]
    height = image.size[1]

    new_image = np.zeros((height, width, 3))

    for x in range(width):
        for y in range(height):
            middle = ((pix[x, y][0] + pix[x, y][1] + pix[x, y][2]) // 3)

            a = middle + k * 2
            b = middle + k
            c = middle
            if (a > 255):
                a = 255
            if (b > 255):
                b = 255
            if (c > 255):
                c = 255

            new_image[y, x, 0] = a
            new_image[y, x, 1] = b
            new_image[y, x, 2] = c

    new_image = np.array(new_image)
    return Image.fromarray(new_image.astype(np.uint8)).convert("RGB")


