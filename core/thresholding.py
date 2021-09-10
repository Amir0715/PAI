from PIL import Image
import numpy as np
from tqdm import tqdm


def kristian_threshold(image: Image.Image, k: float = 0.5, b: int = 3) -> Image.Image:
    width = image.size[0]
    height = image.size[1]

    pix = np.array(image)
    new_image = np.zeros(shape=(height, width, 3))
    # new_image = np.full(shape=(height, width, 3), fill_value=255)
    MinG = pix.min()
    sigma_m = np.zeros(shape=(height, width, 2))
    for x in tqdm(range(width), ascii=True, desc="thresholding"):
        for y in range(height):
            x1 = x - int(b / 2) if x - int(b / 2) > 0 else 0
            x2 = x + int(b / 2) if x + int(b / 2) < width - 1 else width - 1
            y1 = y - int(b / 2) if y - int(b / 2) > 0 else 0
            y2 = y + int(b / 2) if y + int(b / 2) < height - 1 else height - 1

            local_window = pix[y1:y2 + 1, x1:x2 + 1, 0]
            sigma_m[y, x, 0] = local_window.mean()
            sigma_m[y, x, 1] = local_window.std()

    R = sigma_m[:, :, 1].max()
    T = ((1 - k) * sigma_m[:, :, 0]) + (k * MinG) + (k * (sigma_m[:, :, 1] / R) * (sigma_m[:, :, 0] - MinG))
    for x in range(width):
        for y in range(height):
            if pix[y, x, 0] > T[y, x]:
                new_image[y, x] = [255, 255, 255]

    return Image.fromarray(new_image.astype(np.uint8)).convert("RGB")


def binarization(image: Image.Image, T: int = 127) -> Image.Image:
    width = image.size[0]
    height = image.size[1]

    pix = np.array(image)
    new_image = np.zeros_like(pix)

    for x in range(width):
        for y in range(height):
            if image.mode == 'L':
                if pix[y, x] >= T:
                    new_image[y, x] = 255
                else:
                    new_image[y, x] = 0
            elif image.mode == "RGB":
                if pix[y, x, 0] >= T:
                    new_image[y, x, :] = 255
                else:
                    new_image[y, x, :] = 0

    return Image.fromarray(new_image.astype(np.uint8)).convert("L")
