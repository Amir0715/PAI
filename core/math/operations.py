import numpy as np
from PIL import Image


def XOR(image1:Image.Image, image2:Image.Image) -> Image.Image:
    width = image1.size[0]
    height = image1.size[1]
    pix1 = np.array(image1)
    pix2 = np.array(image2)

    new_image = np.zeros(shape=(height, width, 3))

    for x in range(width):
        for y in range(height):
            new_image[y, x] = [255, 255, 255] if (pix1[y, x, 0] or pix2[y, x, 0]) and (not pix1[y, x, 0] or not pix2[y, x, 0]) else [0, 0, 0]

    return Image.fromarray(new_image.astype(np.uint8)).convert("RGB")