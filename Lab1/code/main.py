from PIL import Image, ImageFilter, ImageDraw
from core.resampling import *
from core.halftoning import *
from core.thresholding import *

filename = "downsampling_text.jpg"

original = Image.open("../res/" + filename)

# new_image = resampling(original, 5/2)
# new_image.save("../res/downsampling_" + filename)
#
# new_image = resampling(original, 5)
# new_image.save("../res/upsampling_" + filename)
#
# new_image = resampling(original, 1/4)
# new_image.save("../res/downsampling_" + filename)
# new_image = halftone(original)
# new_image.show()
# new_image.save("../res/halftone" + filename)

# new_image = sepia(original, 30)
# new_image.show()
# new_image.save("../res/sepia_" + filename)
halfton = halftone(original)
# halfton.show()
new_image = kristian_threshold(image=halfton, b=15, k=0.2)
new_image.show()
