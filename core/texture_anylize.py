from PIL import Image
import numpy as np


def get_hararic(img: Image.Image, l: int, d: int, cross=False):
    img_matrix = np.asarray(img).transpose()
    width = img.size[0]
    height = img.size[1]
    matrix = np.zeros((l, l))

    for x in range(d, width - d):
        for y in range(d, height - d):
            pix = img_matrix[x, y]
            if cross:
                first_pix = img_matrix[x - d, y - d]  # up left
                second_pix = img_matrix[x + d, y + d]  # up right
                third_pix = img_matrix[x - d, y + d]  # down right
                fourth_pix = img_matrix[x - d, y - d]  # down left
            else:
                first_pix = img_matrix[x, y - d]  # up
                second_pix = img_matrix[x + d, y]  # right
                third_pix = img_matrix[x, y + d]  # down
                fourth_pix = img_matrix[x - d, y]  # left

            matrix[pix, first_pix] += 1
            matrix[pix, second_pix] += 1
            matrix[pix, third_pix] += 1
            matrix[pix, fourth_pix] += 1

    max_ = np.max(matrix)
    if max_ > 256:
        matrix = (matrix * 256) // max_

    return Image.fromarray(matrix).convert('L'), matrix


def attribute(matrix):
    asm = np.sum(matrix ** 2)  # энергия

    con = 0  # котрастность

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            con += ((i - j) ** 2) * matrix[i][j]

    mpr = np.max(matrix)  # максимальная вероятность

    lun = 0  # локальная однородность
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            lun += matrix[i][j] / (1 + ((i - j) ** 2))

    sub_matrix = matrix.copy()
    sub_matrix[sub_matrix == 0] = 1
    ent = -np.sum(np.multiply(np.log2(sub_matrix), matrix))  # энтропия

    tr = np.sum(np.diagonal(matrix))  # след матрицы

    p_j = np.sum(matrix, axis=0)  # вспомогательные векторы
    p_i = np.sum(matrix, axis=1)
    mean_i = (np.arange(1, 257) * p_i).sum()  # мат ожидание
    mean_j = (np.arange(1, 257) * p_j).sum()

    av = 0  # среднее значение серого
    for i, item in enumerate(p_i):
        av += i * item

    sigma_i, sigma_j = 0, 0
    for i in range(1, 257):
        sigma_i += (i - mean_j) ** 2 * p_i[i - 1]
        sigma_j += (i - mean_i) ** 2 * p_j[i - 1]

    corr = 0  # корреляция значений яркости
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            corr += i*j*matrix[i][j]

    corr -= av**2
    corr /= (sigma_i ** 0.5) * (sigma_j ** 0.5)
    return {
        "asm": asm,
        "mpr": mpr,
        "ent": ent,
        "tr": tr,
        "con": con,
        "lun": lun,
        "av": av,
        "corr": corr
    }


def add_to_report(report_file, img_src: str, img_res: str, attrs: list[str], attributes):
    report_file.write("### Исходное изображение\n\n")
    report_file.write(f"![]({img_src})\n\n")
    report_file.write("### Матрица Харалика\n\n")
    report_file.write(f"![]({img_res})\n\n")
    for attr in attrs:
        report_file.write(f"{attr}: {attributes[attr]}\n\n")

    report_file.write("\n\n")
