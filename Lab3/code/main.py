import numpy as np
from PIL import Image
from tqdm import tqdm

from core.gradients import gradient
from core.halftoning import halftone
from core.thresholding import kristian_threshold, binarization

operator_gx = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
operator_gy = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])

# operator_gx = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
# operator_gy = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
# myimage = Image.fromarray(np.array([
#     [20, 45, 60, 90, 120],
#     [10, 20, 50, 80, 130],
#     [30, 60, 80, 100, 160],
#     [60, 80, 140, 190, 180],
#     [70, 90, 160, 200, 255]
# ]).astype(np.uint8)).convert("L")
# print("myimage : \n", np.array(myimage))
# # myimage.show()
# semitone = halftone(myimage)
# # semitone.show()
# print("semiton : \n", np.array(semitone))
# gradx, grady, grad, bin_image = gradient(semitone, operator_gx, operator_gy)
# print("gradx : \n", gradx)
# print()
# print("grady : \n", grady)
# print()
# print("grad : \n", grad)
# print()
# print("bin_image : \n", bin_image)
T = 124 # парметр границы для бинаризации
PREFIX = 'Lab3'

filename = "castel.jpg"

original = Image.open(f"original/" + filename)

semitone = np.array(halftone(original))

semitone = Image.fromarray(semitone.astype(np.uint8)).convert("RGB")

semitone.save(f"{PREFIX}/res/semitone_" + filename)

gradx, grady, grad = gradient(semitone, operator_gy, operator_gx)

resx = Image.fromarray(gradx.astype(np.uint8)).convert("RGB")
resy = Image.fromarray(grady.astype(np.uint8)).convert("RGB")
res = Image.fromarray(grad.astype(np.uint8)).convert("RGB")


resx.save(f"{PREFIX}/res/resx_{filename}")
resy.save(f"{PREFIX}/res/resy_{filename}")
res.save(f"{PREFIX}/res/res_{filename}")

for t in tqdm(range(120, 145, 2)):
    bin = binarization(res, t)
    bin.save(f"{PREFIX}/res/bin_t{t}_{filename}")
