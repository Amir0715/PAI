import numpy as np
from PIL import Image


def windowing(image: Image.Image, x: int, y: int, b: int) -> np.ndarray:
    new_image = np.array(image)
    width = image.size[0]
    height = image.size[1]

    x1 = x - int(b / 2) if x - int(b / 2) > 0 else 0
    x2 = x + int(b / 2) if x + int(b / 2) < width - 1 else width - 1
    y1 = y - int(b / 2) if y - int(b / 2) > 0 else 0
    y2 = y + int(b / 2) if y + int(b / 2) < height - 1 else height - 1

    new_image = new_image[y1:y2 + 1, x1:x2 + 1, :]
    return new_image
