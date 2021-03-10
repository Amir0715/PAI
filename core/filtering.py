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
