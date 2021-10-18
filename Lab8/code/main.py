import os
from itertools import product

from PIL import Image
from tqdm import tqdm

from core.contrasting import linear_contrasting, get_gist

workspace = "Lab8"
names = [f"{x}" for x in range(1, 7)]
for name in names:
    filename = f"{name}.jpg"

    img = Image.open(f"{workspace}/assets/{filename}").convert("L")

    # Создаем каталог для результатов гистограмм данного изображения
    if not os.path.isdir(f"{workspace}/res/hist/{name}"):
         os.mkdir(f"{workspace}/res/hist/{name}")
         os.mkdir(f"{workspace}/res/hist/{name}/original")

    # Сохроняем оригинальную гистограмму
    get_gist(img, f"{workspace}/res/hist/{name}/original/{filename}")

    if not os.path.isdir(f"{workspace}/res/hist/{name}"):
        os.mkdir(f"{workspace}/res/hist/{name}")
    if not os.path.isdir(f"{workspace}/res/img/{name}"):
        os.mkdir(f"{workspace}/res/img/{name}")

    # Список кортежей длинной 2 которые были полученны декартовым произведением двух списков
    args = [_ for _ in product(list(range(0, 245, 20)), list(range(20, 255, 20)))]
    # args = [(x, x+5) for x in range(0, 250, 5)]
    for arg in tqdm(args, desc=f"{name}"):

        if not os.path.isdir(f"{workspace}/res/hist/{name}/min_{arg[0]}"):
            os.mkdir(f"{workspace}/res/hist/{name}/min_{arg[0]}")
        if not os.path.isdir(f"{workspace}/res/hist/{name}/min_{arg[0]}/max_{arg[1]}"):
            os.mkdir(f"{workspace}/res/hist/{name}/min_{arg[0]}/max_{arg[1]}")
        if not os.path.isdir(f"{workspace}/res/img/{name}/min_{arg[0]}"):
            os.mkdir(f"{workspace}/res/img/{name}/min_{arg[0]}")
        if not os.path.isdir(f"{workspace}/res/img/{name}/min_{arg[0]}/max_{arg[1]}"):
            os.mkdir(f"{workspace}/res/img/{name}/min_{arg[0]}/max_{arg[1]}")

        result_img = linear_contrasting(img, *arg)
        result_img.save(f"{workspace}/res/img/{name}/min_{arg[0]}/max_{arg[1]}/{filename}")
        get_gist(result_img, f"{workspace}/res/hist/{name}/min_{arg[0]}/max_{arg[1]}/hist.jpg")
