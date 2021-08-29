import csv

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from core.highlithing import cut_letter
from core.thresholding import binarization

LETTERS = [char[0] for char in open('Lab4/code/letters.txt', 'r')]


def generate(letters: list, font, folderpath: str, size=(52, 52)):
    for letter in letters:
        limag = Image.new(mode='L', size=size, color="white")
        draw = ImageDraw.Draw(limag)
        draw.text(xy=(0, 0), font=font, text=letter, fill="black")
        limag = binarization(limag)
        limag = cut_letter(limag)
        path = folderpath + f'/{letter}.png'
        limag.save(path)


def report():
    with open('Lab4/res/data.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        with open('Lab4/README.md', 'a+') as file:
            next(reader)
            for (i, letter), row in zip(enumerate(LETTERS), reader):
                file.write(
                    f"""
### Буква {letter}
|Символ|Профиль по х|Профиль по y|
|---------------------|--------------------------|--------------------------|
|![](../letters/{letter}.png)| ![](res/profiles/x/{letter}.png)| ![](res/profiles/y/{letter}.png)|
"""
                )

                file.write(
                    f"""
|Признак|Значение|
|-------|--------|
|Вес чёрного|{row[1]}|
|Нормированный вес чёрного|{row[2]}|
|Центр масс|{row[3]}|
|Нормированный центр масс|{row[4]}|
|Моменты инерции|{row[5]}|
|Нормированные моменты инерции|{row[6]}|
"""
                )


if __name__ == '__main__':
    report()
