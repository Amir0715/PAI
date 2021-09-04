import numpy as np
from PIL import Image
from core import halftoning
from core import texture_anylize

m = 0
n = 0
l = 256
d = 1
cross = False
images_name = [f'{i}.jpg' for i in range(1, 7)]
attrs = ['corr']
work_space = 'Lab7'

with open('Lab7/README.md', mode='w') as file:
    for name in images_name:
        img_src_path = f"{work_space}/assets/{name}"
        img = Image.open(img_src_path)
        img = halftoning.halftone(img)
        img.save(f'{work_space}/res/halftone/{name}')

        img_res, matrix_res = texture_anylize.get_hararic(img, l, d, cross)
        img_res.convert('L').save(f"{work_space}/res/hararic/{name}")

        k = np.sum(matrix_res)
        norm_matrix_res = matrix_res / k
        attributes = texture_anylize.attribute(norm_matrix_res)

        texture_anylize.add_to_report(file, f"assets/{name}", f"res/hararic/{name}", attrs, attributes)
