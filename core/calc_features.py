import csv
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image


def black_weight(image: Image.Image):
    width = image.size[0]
    height = image.size[1]
    pix = np.array(image)
    weight = 0
    for x in range(width):
        for y in range(height):
            if not np.all(pix[y, x]):
                weight += 1
    return weight


def unit_black_weight(image: Image.Image):
    return black_weight(image) / image.size[0] * image.size[1]


def calc_features(image: Image.Image, letter: str):
    weight = black_weight(image)
    rel_weight = unit_black_weight(image)
    image = np.array(image)
    img_b = np.zeros(shape=image.shape)

    img_b[image != 255] = 1
    x_avg = 0
    for x, column in enumerate(img_b.T):
        x_avg += np.sum((x + 1) * column)
    rel_x_avg = (x_avg - 1) / (weight - 1)

    y_avg = 0
    for y, row in enumerate(img_b):
        y_avg += np.sum((y + 1) * row)
    rel_y_avg = (y_avg - 1) / (weight - 1)

    iner_x = 0
    for y, row in enumerate(img_b):
        iner_x += np.sum((y + 1 - y_avg) ** 2 * row)
    rel_iner_x = iner_x / (img_b.shape[0] ** 2 + img_b.shape[1] ** 2)

    iner_y = 0
    for x, column in enumerate(img_b.T):
        iner_y += np.sum((x + 1 - x_avg) ** 2 * column)
    rel_iner_y = iner_y / (img_b.shape[0] ** 2 + img_b.shape[1] ** 2)

    return {
        "letter": letter,
        "weight": weight,
        "rel_weight": rel_weight,
        "center": (x_avg, y_avg),
        "rel_center": (rel_x_avg, rel_y_avg),
        "inertia": (iner_x, iner_y),
        "rel_inertia": (rel_iner_x, rel_iner_y)
    }


# TODO: done profiles
def profile_x(image: Image.Image, char: str, opath: str):
    image = np.array(image)
    image[image <= 127] = 1
    image[image > 127] = 0
    prof_y = np.sum(image, axis=0)
    prof_x = np.arange(start=1, stop=image.shape[1] + 1).astype(int)
    plt.bar(x=prof_x, height=prof_y)
    plt.ylim(0, image.shape[0] + 1)
    plt.xlim(0, image.shape[1] + 1)
    plt.savefig(f'{opath}/profiles/x/{char}.png')
    plt.clf()


def profile_y(image: Image.Image, char: str, opath: str):
    image = np.array(image)
    image[image <= 127] = 1
    image[image > 127] = 0
    prof_y = np.sum(image, axis=1)
    prof_x = np.arange(start=1, stop=image.shape[0] + 1).astype(int)

    plt.barh(y=prof_x, width=prof_y)

    plt.ylim(image.shape[0] + 1, 0)
    plt.xlim(0, image.shape[1] + 1)
    plt.savefig(f'{opath}/profiles/y/{char}.png')
    plt.clf()


if __name__ == '__main__':
    method_prefix = 'Image_Features'
    LETTERS = [char[0] for char in open('Lab4/code/letters.txt', 'r')]
    with open('Lab4/res/data.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['letter', 'weight', 'rel_weight', 'center',
                                                     'rel_center', 'inertia', 'rel_inertia'])
        writer.writeheader()

        for letter in LETTERS:
            img = Image.open(f'letters/{letter}.png').convert('L')

            writer.writerow(calc_features(img, letter))
