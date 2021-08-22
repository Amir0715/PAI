import os
import glob

import numpy
from PIL import ImageChops, Image

from core.calc_features import profile_x, profile_y
from core.utils import segmentation, gen_report

img = Image.open(f'Lab5/assets/sentence.png').convert("L")

invert_img = ImageChops.invert(img)

if not os.path.isfile('Lab5/assets/invert_sentence.png'):
    invert_img.save(f'Lab5/assets/invert_sentence.png')

profile_x(img, 'sentence', 'Lab5/res')
profile_y(img, 'sentence', 'Lab5/res')

segmentation(img, 'Lab5/res/segmentation/chars')

img_chars = glob.glob('Lab5/res/segmentation/chars/*.png')
print(len(img_chars))

for i, img_char in enumerate(img_chars):
    img = Image.open(img_char).convert("L")
    profile_x(img, f'{i}', 'Lab5/res/segmentation')
    profile_y(img, f'{i}', 'Lab5/res/segmentation')

gen_report(len(img_char))