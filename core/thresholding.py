from PIL import Image
import numpy as np

def kristian_threshold(image : Image.Image) -> Image.Image:
    b = 10 # размер локального окна b*b

    width = image.size[0]
    height = image.size[1]

    bx : np.ndarray = np.ogrid[0:width:b]
    np.append(bx, width)
    print(bx)

    return image
