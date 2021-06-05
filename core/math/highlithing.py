import numpy as np
from PIL import Image

def cut_letter(binimage: Image.Image):
    width = binimage.size[0]
    height = binimage.size[1]

    x2 = 0
    x1 = width
    y2 = 0
    y1 = height

    pix = np.array(binimage)

    for x in range(width):
        for y in range(height):
            if pix[y, x, 0] == 0:
                if x >= x2:
                    x2 = x
                if x < x1:
                    x1 = x
                if y >= y2:
                    y2 = y
                if y < y1:
                    y1 = y

    newimage = np.zeros((y2-y1+1, x2-x1+1, 3))
    i = j = 0
    for x in range(x1, x2+1):
        for y in range(y1, y2+1):
            newimage[i, j] = pix[y, x]
            i += 1
        j += 1
        i = 0

    return Image.fromarray(newimage.astype(np.uint8)).convert("RGB")

