import os

import cv2
import numpy as np
from tqdm import tqdm

cap = cv2.VideoCapture("VIDEO1.mp4")
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

if not os.path.exists('data'):
    os.makedirs('data')

out = cv2.VideoWriter(
    './data/output.avi',
    cv2.VideoWriter_fourcc(*'MJPG'),   # codec
    25.0,  # fps
    (1280, 720),  # width, height
    isColor=True)

currentframe = 0
k = 30

time_length = 6.0 * 60.0 + 41.0
fps = 25
frame_seq = 5350
frame_no = (frame_seq / (time_length * fps))

cap.set(cv2.CAP_PROP_POS_FRAMES, 5350-1)

for i in tqdm(range(100)):
    ret, frame = cap.read()
    # print(frame)
    # frame = sepia_np(np.array(frame))
    pix = np.array(frame)
    width = pix.shape[1]
    height = pix.shape[0]

    new_image = np.zeros((height, width, 3))

    for x in range(width):
        for y in range(height):
            middle = (frame[y, x][0]/3 + frame[y, x][1]/3 + frame[y, x][2]/3)

            r = middle + k * 2
            g = middle + k
            b = middle
            if r > 255:
                r = 255
            if b > 255:
                b = 255
            if g > 255:
                g = 255

            new_image[y, x, 0] = b
            new_image[y, x, 1] = g
            new_image[y, x, 2] = r

    new_image = new_image.astype('uint8')
    # name = './data/frame' + str(i) + 'o.jpg'
    # cv2.imwrite(name, frame)
    # name = './data/frame' + str(i) + '.jpg'
    # cv2.imwrite(name, new_image)
    out.write(new_image)

cap.release()
out.release()
cv2.destroyAllWindows()
