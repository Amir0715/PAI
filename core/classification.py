from math import sqrt

from core.calc_features import *


def euclidean_distance(image_a, image_b):
    center_x_a, center_y_a = normalized_gravity_center(image_a)
    center_x_b, center_y_b = normalized_gravity_center(image_b)
    return sqrt(
    ((unit_black_weight(image_a) - unit_black_weight(image_b)) ** 2) +
    ((center_x_a - center_x_b) ** 2) +
    ((center_y_a - center_y_b) ** 2) +
    ((normalized_central_vertical_axial_moment(image_a) - normalized_central_vertical_axial_moment(image_b)) ** 2) +
    ((normalized_central_horizontal_axial_moment(image_a) - normalized_central_horizontal_axial_moment(image_b)) ** 2)
    )


def find_match(local_letter: Image.Image, standard_letters: list[tuple[str, Image.Image]]) -> dict:
    result = {}
    for standard_letter in standard_letters:
        result[standard_letter[0]] = euclidean_distance(local_letter, standard_letter[1])

    return dict(sorted(result.items(), key=lambda item: item[1], reverse=True))