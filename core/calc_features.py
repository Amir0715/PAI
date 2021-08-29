import csv
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image


def black_weight(image: Image.Image) -> int:
    # вес черного
    weight = 0
    for x in range(image.width):
        for y in range(image.height):
            pixel = image.getpixel((x, y))
            if pixel < 127:
                weight += 1
    return weight


def unit_black_weight(image: Image.Image) -> float:
    # удельный вес черного
    return black_weight(image) / (image.size[0] * image.size[1])


def gravity_center(image: Image.Image) -> (int, int):
    # Абсолютные координаты центра тяжести
    x_coord = 0
    y_coord = 0

    for x in range(image.width):
        for y in range(image.height):
            pixel = image.getpixel((x, y))
            if pixel < 127:
                pixel = 1
            else:
                pixel = 0
            x_coord += x * pixel
            y_coord += y * pixel

    weight = black_weight(image)
    return int(round(x_coord / weight)), int(round(y_coord / weight))


def normalized_gravity_center(image: Image.Image) -> (float, float):
    # Нормированные координаты центра тяжести
    x, y = gravity_center(image)
    return (x - 1) / (image.width - 1), (y - 1) / (image.height - 1)


def central_horizontal_axial_moment(image: Image.Image):
    # Абсолютно горизонатальный осевой моменты инерции
    center_x, center_y = gravity_center(image)
    result = 0

    for x in range(image.width):
        for y in range(image.height):
            pixel = image.getpixel((x, y))
            if pixel < 127:
                pixel = 1
            else:
                pixel = 0
            result += ((y - center_y) ** 2) * pixel

    return result


def normalized_central_horizontal_axial_moment(image: Image.Image):
    # Норм горизонатальный осевой моменты инерции
    return central_horizontal_axial_moment(image) / (image.width ** 2 + image.height ** 2)


def central_vertical_axial_moment(image: Image.Image):
    # Абсолютно вертикальный осевой моменты инерции
    center = gravity_center(image)
    result = 0

    for x in range(image.width):
        for y in range(image.height):
            pixel = image.getpixel((x, y))
            if pixel < 127:
                pixel = 1
            else:
                pixel = 0
            result += ((x - center[0]) ** 2) * pixel

    return result


def normalized_central_vertical_axial_moment(image: Image.Image):
    # Норм вертикальный осевой моменты инерции
    return central_vertical_axial_moment(image) / (image.width ** 2 + image.height ** 2)


def central_i45_axial_moment(image: Image.Image):
    x_center, y_center = gravity_center(image)
    i45_center = 0
    for x in range(image.width):
        for y in range(image.height):
            pixel = image.getpixel((x, y))
            if pixel < 127:
                pixel = 1
            else:
                pixel = 0
            i45_center += (((y - y_center - x + x_center) ** 2) * pixel) / 2

    return i45_center


def normalized_central_i45_axial_moment(image: Image.Image):
    return central_i45_axial_moment(image) / (image.width ** 2 + image.height ** 2)


def central_i135_axial_moment(image: Image.Image):
    x_center, y_center = gravity_center(image)
    i135_center = 0
    for x in range(image.width):
        for y in range(image.height):
            pixel = image.getpixel((x, y))
            if pixel < 127:
                pixel = 1
            else:
                pixel = 0
            i135_center += (((y - y_center + x - x_center) ** 2) * pixel) / 2

    return i135_center


def normalized_central_i135_axial_moment(image: Image.Image):
    return central_i135_axial_moment(image) / (image.width ** 2 + image.height ** 2)


def calc_features(image: Image.Image, letter: str):
    return {
        "letter": letter,
        "weight": black_weight(image),
        "rel_weight": unit_black_weight(image),
        "center": gravity_center(image),
        "rel_center": normalized_gravity_center(image),
        "horizontal moment": central_horizontal_axial_moment(image),
        "vertical moment": central_vertical_axial_moment(image),
        "normalized horizontal moment": normalized_central_horizontal_axial_moment(image),
        "normalized vertical moment": normalized_central_vertical_axial_moment(image),
        "i45 moment": central_i45_axial_moment(image),
        "normalized i45 moment": normalized_central_i45_axial_moment(image),
        "i135 moment": central_i135_axial_moment(image),
        "normalized i135 moment": normalized_central_i135_axial_moment(image),
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


def export_csv(opath: str, letters, images_folder: str, mode='w', file=True):
    if file:
        LETTERS = [char[0] for char in open(letters, 'r')]
    else:
        LETTERS = letters
    with open(opath, mode, newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['letter', 'weight', 'rel_weight', 'center',
                                                     'rel_center', 'horizontal moment', 'vertical moment',
                                                     "normalized horizontal moment",
                                                     "normalized vertical moment",
                                                     "i45 moment",
                                                     "normalized i45 moment",
                                                     "i135 moment",
                                                     "normalized i135 moment"])
        writer.writeheader()
        for letter in LETTERS:
            img = Image.open(f'{images_folder}/{letter}.png').convert('L')
            writer.writerow(calc_features(img, letter))


if __name__ == '__main__':
    method_prefix = 'Image_Features'
    export_csv("Lab6/assets/data.csv", "Lab6/assets/letters.txt", "letters")
