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


def get_profiles(img):
    width = img.size[0]
    height = img.size[1]
    x_profiles = []
    y_profiles = []

    for x in range(width):
        bright = 0
        for y in range(height):
            pix = img.getpixel((x, y))
            if pix == 0:
                bright += 1
        x_profiles.append(bright)

    for y in range(height):
        bright = 0
        for x in range(width):
            pix = img.getpixel((x, y))
            if pix == 0:
                bright += 1
        y_profiles.append(bright)

    return x_profiles, y_profiles


def segmentation(img, opath):
    height = img.size[1]
    x_profiles, y_profiles = get_profiles(img)
    ep = 0
    res = []
    for i in range(len(x_profiles)):

        if x_profiles[i] <= ep:
            step = 0
        else:
            step += 1
            right = i
            left = right - step
            if x_profiles[i + 1] <= ep:
                res.append((left, right))

    for i in range(len(res)):
        left, right = res[i]
        new_im = img.crop((left, 0, right + 2, height))
        new_im = reference_image(new_im)
        new_im.save(f"{opath}/" + str(i) + ".png", mode="1")
    return res


def reference_image(img):
    pix = img.load()
    width, height = img.size[0], img.size[1]
    hor_p = [0 for _ in range(width)]
    ver_p = [0 for _ in range(height)]
    for i in range(width):
        for j in range(height):
            if pix[i, j] == 0:
                hor_p[i] += 1
                ver_p[j] += 1
    x0, y0, x1, y1 = 0, 0, width, height
    eps = 0
    for i in range(width):
        if hor_p[i] > eps:
            x0 = i
            break

    for i in range(width - 1, -1, -1):
        if hor_p[i] <= eps:
            x1 = i
        else:
            break

    for i in range(height):
        if ver_p[i] > eps:
            y0 = i
            break

    for i in range(height - 1, -1, -1):
        if ver_p[i] <= eps:
            y1 = i
        else:
            break

    new_sz = (x0, y0, x1, y1)
    return img.crop(new_sz)


def gen_report(letters: list):
    with open('Lab5/README.md', 'w') as file:
        for letter in range(len(letters)):
            file.write(
                f"""
### Буква №{letter}
|Символ|Профиль по х|Профиль по y|
|---------------------|--------------------------|--------------------------|
|![](res/segmentation/chars/{letter}.png)| ![](res/segmentation/profiles/x/{letter}.png)| ![](res/segmentation/profiles/y/{letter}.png)|
"""
            )