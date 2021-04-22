import glob
from PIL import Image, ImageFont
from core.calc_features import *
from core.generate import generate

# foldepath = '/home/amir-kamolov/PycharmProjects/PAI/letters'
#
LETTERS = [char[0] for char in open('Lab4/code/letters.txt', 'r')]
#
# font = ImageFont.truetype("/home/amir-kamolov/PycharmProjects/PAI/fonts/Sylfaen.ttf", size=52)
# generate(letters, font, foldepath)

chars = glob.glob("letters/*.png")
for char in LETTERS:
    image_char = Image.open(f"letters/{char}.png").convert("L")
    black_weight(image_char)
    unit_black_weight(image_char)
    calc_features(image_char, char)
    profile_x(image_char, char)
    profile_y(image_char, char)