from PIL import Image
import os.path

from core.filtering import median
from core.halftoning import halftone
from core.operations import XOR
from core.thresholding import kristian_threshold

filename = "screenshot.png"
B = 15
K = 0.2
# if not os.path.exists("../res/threshold_B" + str(B) + "K" + str(K).replace('.', '') + "_" + filename):
#     original = Image.open("../original/" + filename)
#     halftone_f2 = halftone(original)
#     threshold = kristian_threshold(image=halftone_f2, b=B, k=K)
#     threshold.save("../res/threshold_B" + str(B) + "K" + str(K).replace('.', '') + "_" + filename)
#     print("Done threshold")
#
# original = Image.open("../res/threshold_B" + str(B) + "K" + str(K).replace('.', '') + "_" + filename)

original = Image.open("../original/" + filename)

hill_core = \
    [[1, 2, 1],
     [2, 4, 2],
     [1, 2, 1]]
depression_core = \
    [[4, 2, 4],
     [3, 1, 3],
     [4, 2, 4]]

median_depression = median(original, depression_core)
median_depression.save("../res/median_depression_" + filename)
print("Done median_depression")

xor_depression = XOR(original, median_depression)
xor_depression.save("../res/xor_depression_" + filename)
print("Done XOR median_depression")

median_hill = median(original, hill_core)
median_hill.save("../res/median_hill_" + filename)
print("Done median_hill")

xor_hill = XOR(original, median_hill)
xor_hill.save("../res/xor_hill_" + filename)
print("Done XOR median_hill")

xor = XOR(median_depression, median_hill)
xor.save("../res/xor_hill_depression_" + filename)
print("Done XOR hill_depression")
