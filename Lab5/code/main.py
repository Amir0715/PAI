import glob
from PIL import ImageChops, Image

from core.calc_features import profile_x, profile_y
from core.utils import segmentation, gen_report
from core.thresholding import binarization
img = Image.open(f'Lab5/assets/sentence.png').convert("L")
img = binarization(img)
invert_img = ImageChops.invert(img)
invert_img.save(f'Lab5/assets/invert_sentence.png')

profile_x(img, 'sentence', 'Lab5/res')
profile_y(img, 'sentence', 'Lab5/res')

segmentation(img, 'Lab5/res/segmentation/chars')

img_chars = glob.glob('Lab5/res/segmentation/chars/*.png')
print(len(img_chars))

for img_char in img_chars:
    i = img_char.split('/')[-1].split('.')[0]
    img = Image.open(img_char).convert("L")
    profile_x(img, f'{i}', 'Lab5/res/segmentation')
    profile_y(img, f'{i}', 'Lab5/res/segmentation')

gen_report(img_chars)