import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

from core.halftoning import halftone


def calculate_brightness(f, f_min, f_max, g_min, g_max):
    return round(int((f - f_min) / (f_max - f_min) * (g_max - g_min) + g_min))


def linear_contrasting(image: Image.Image, min_brightness: int = 0, max_brightness: int = 255) -> Image.Image:
    image_pixels = list(image.getdata())

    image_min_brightness = min(image_pixels)
    image_max_brightness = max(image_pixels)

    result = image.copy()

    for x in range(result.width):
        for y in range(result.height):
            brightness = calculate_brightness(result.getpixel((x, y)), image_min_brightness, image_max_brightness,
                                              min_brightness, max_brightness)
            result.putpixel((x, y), brightness)

    return result


def get_gist(img: Image.Image, path:str):
    semitone = np.array(halftone(img))
    sh = np.reshape(semitone, (1, -1))
    plt.hist(sh[0], bins=256)
    plt.savefig(path)
    plt.clf()