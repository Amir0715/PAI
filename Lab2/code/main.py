from PIL import Image, ImageChops
import os.path

from core.filtering import median
from core.halftoning import halftone
from core.operations import XOR
from core.thresholding import kristian_threshold
from core.filtering import add_salt_and_pepper

filename = "cat2.jpg"
B = 15
K = 0.2
s_vs_p = 0.5
amount = 0.05
save_dir = f"Lab2/res/{filename}_svsp{s_vs_p}_amount{amount}"
threshold_name = f"{save_dir}/threshold_B{B}K{K}_{filename}"

try:
    os.mkdir(save_dir)
except OSError:
    pass

if not os.path.exists(threshold_name):
    original = Image.open("original/" + filename)
    halftone_f2 = halftone(original.convert("L").convert("RGB"))
    threshold = kristian_threshold(image=halftone_f2, b=B, k=K)
    threshold.save(threshold_name)
    print("Done threshold")

original = Image.open(threshold_name)

original_with_salt = add_salt_and_pepper(original, amount, s_vs_p)
original_with_salt.save(f"{save_dir}/with_salt_{s_vs_p}_{amount}_{filename}")

hill_core = \
    [[1, 2, 1],
     [2, 4, 2],
     [1, 2, 1]]
depression_core = \
    [[4, 2, 4],
     [3, 1, 3],
     [4, 2, 4]]

median_depression = median(original_with_salt, depression_core)
median_depression.save(f"{save_dir}/median_depression_{s_vs_p}_{amount}_{filename}")
print("Done median_depression")

xor_depression = ImageChops.logical_xor(original_with_salt.convert("1"), median_depression.convert("1"))
# xor_depression = XOR(original_with_salt, median_depression)
xor_depression.save(f"{save_dir}/xor_depression_{s_vs_p}_{amount}_{filename}")
print("Done XOR median_depression")

median_hill = median(original_with_salt, hill_core)
median_hill.save(f"{save_dir}/median_hill_{s_vs_p}_{amount}_{filename}")
print("Done median_hill")

xor_hill = ImageChops.logical_xor(original_with_salt.convert("1"), median_hill.convert("1"))
# xor_hill = XOR(original_with_salt, median_hill)
xor_hill.save(f"{save_dir}/xor_hill_{s_vs_p}_{amount}_{filename}")
print("Done XOR median_hill")

xor = ImageChops.logical_xor(median_depression.convert("1"), median_hill.convert("1"))
# xor = XOR(median_depression, median_hill)
xor.save(f"{save_dir}/xor_hill_depression_{s_vs_p}_{amount}_{filename}")
print("Done XOR hill_depression")
