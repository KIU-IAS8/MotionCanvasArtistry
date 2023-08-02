import cv2

from tools.camera_integration import VideoCapture
from maths.constants.matrices import *
from maths.functions.filters import *


vc = VideoCapture()
vc.display_live_camera_signal()

data = vc.convert_to_grayscale()
new_image = sobel_filter(frame=data, filter=SOBEL_Y, padding=0, strides=1)


cv2.imwrite("tools/img2.png", new_image)
