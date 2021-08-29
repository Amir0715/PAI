from PIL import Image, ImageFont
import glob

from core.calc_features import export_csv
from core.classification import find_match
from core.generate import generate
from core.utils import segmentation


LETTERS = [char[0] for char in open('Lab6/assets/letters.txt', 'r', encoding="UTF-8")]
font = ImageFont.truetype("/home/amir/projects/PAI/fonts/Sylfaen.ttf", size=52)
generate(LETTERS, font, 'Lab6/assets/default_chars')
export_csv("Lab6/assets/default_data.csv", LETTERS, "Lab6/assets/default_chars", file=False)

sentence = Image.open("Lab6/assets/sentence2.png").convert('L')
segmentation(sentence, 'Lab6/res/segmentation/chars')
global_chars = glob.glob('Lab6/assets/default_chars/*.png')
local_chars = glob.glob('Lab6/res/segmentation/chars/*.png')
global_chars_tuple = list()

for global_char in global_chars:
    char = global_char.split('/')[-1].split('.')[0]
    global_chars_tuple.append((char, Image.open(global_char)))

with open('Lab6/README.md', mode='a') as file:
    file.write("## Оценка близости для размера шрифта 52\n\n")
    file.write("")
    for i, local_char in enumerate(local_chars):
        rows = find_match(Image.open(local_char), global_chars_tuple)
        file.write(f"### Буква {i}\n\n![]({'/'.join(local_char.split('/')[1:])})\n\n")
        file.write(f"## Лучшие гипотезы: \n\n")
        file.write(f"| Буква | Близость |\n")
        file.write(f"| :---: | :---: |\n")
        for row in rows.items():
            file.write(f"|{row[0]}|{row[1]}|\n")
        file.write("\n")