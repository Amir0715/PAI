import numpy as np
from PIL import Image

from core.gradients import gradient
from core.halftoning import halftone
from core.thresholding import kristian_threshold

# operator_gx = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
# operator_gy = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])

operator_gx = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
operator_gy = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])

PREFIX = '..'

filename = "screenshot.png"

original = Image.open(f"{PREFIX}/original/" + filename)

semitone = np.array(halftone(original))

Image.fromarray(semitone.astype(np.uint8)).convert("RGB").save(f"{PREFIX}/res/semitone_"+filename)

gradx, grady, grad, bin_image = gradient(semitone, operator_gx, operator_gy)

resx = Image.fromarray(gradx.astype(np.uint8)).convert("RGB")
resy = Image.fromarray(grady.astype(np.uint8)).convert("RGB")
res = Image.fromarray(grad.astype(np.uint8)).convert("RGB")
resbin_image = Image.fromarray(bin_image.astype(np.uint8)).convert("RGB")
resx.save(f"{PREFIX}/res/resx.jpg")
resy.save(f"{PREFIX}/res/resy.jpg")
res.save(f"{PREFIX}/res/res.jpg")
resbin_image.save(f"{PREFIX}/res/resbin.jpg")

