import numpy as np
from PIL import Image
from tqdm import tqdm


def median(original: Image.Image, core: list) -> Image.Image:
    width = original.size[0]
    height = original.size[1]
    core = np.array(core)
    # print(core)
    b = len(core)  # размер окна
    pix = np.array(original)
    new_image = np.copy(pix)

    for x in tqdm(range(int(b / 2), width - int(b / 2)), ascii=True, desc="median_filtering"):
        for y in range(int(b / 2), height - int(b / 2)):
            # индексы окна
            x1 = x - int(b / 2) if x - int(b / 2) > 0 else 0
            x2 = x + int(b / 2) if x + int(b / 2) < width - 1 else width - 1
            y1 = y - int(b / 2) if y - int(b / 2) > 0 else 0
            y2 = y + int(b / 2) if y + int(b / 2) < height - 1 else height - 1

            local_window: np.ndarray = pix[y1:y2 + 1, x1:x2 + 1, 0]
            local_window = local_window * core  # окно после умножения на коэф. ядра
            local_window[local_window > 255] = 255
            med = np.median(local_window)
            med = int(med)
            new_image[y, x] = med

    return Image.fromarray(new_image.astype(np.uint8)).convert("RGB")


def add_salt_and_pepper(image : Image.Image, amount: float = 0.005, s_vs_p: float = 0.5) -> Image.Image:
    image = np.array(image)
    row, col, ch = image.shape
    out = np.copy(image)
    # Salt mode
    num_salt = np.ceil(amount * image.size * s_vs_p)
    coords = [np.random.randint(0, i - 1, int(num_salt))
              for i in image.shape]
    out[coords] = 1

    # Pepper mode
    num_pepper = np.ceil(amount * image.size * (1. - s_vs_p))
    coords = [np.random.randint(0, i - 1, int(num_pepper))
              for i in image.shape]
    out[coords] = 0

    return Image.fromarray(out.astype(np.uint8)).convert("L").convert("RGB")

def gauss_noise(image: Image.Image) -> Image.Image:
    image = np.array(image)
    row, col, ch = image.shape
    mean = 0
    var = 0.5
    sigma = var ** 0.9
    gauss = np.random.normal(mean, sigma, (row, col, ch))
    gauss = gauss.reshape(row, col, ch)
    out = image + gauss
    return Image.fromarray(out.astype(np.uint8)).convert("RGB")
