from PIL import Image, ImageFilter, ImageDraw
from core.resampling import *
from core.halftoning import *
from core.thresholding import *

filename = "cat2.jpg"

original = Image.open("original/" + filename)

# new_image = resampling(original, 5/2)
# new_image.save("../res/downsampling_" + filename)
#
# new_image = resampling(original, 5)
# new_image.save("../res/upsampling_" + filename)
#
new_image1 = resampling(original, 1/2)
new_image1.save("Lab1/res/downsampling_" + filename)
# new_image = halftone(original)
# new_image.show()
# new_image.save("../res/halftone" + filename)

# new_image = sepia(original, 30)
# new_image.show()
# new_image.save("../res/sepia_" + filename)

halfton = halftone(new_image1)
B = [20, 40, 80]
K = [0.2, .6, 0.8]

for b, k in [(b, k) for b in B for k in K]:
    print(b, k)
    new_image = kristian_threshold(image=halfton, b=b, k=k)
    new_image.save(f"Lab1/res/threshold_b{b}_k{k}_{filename}")
