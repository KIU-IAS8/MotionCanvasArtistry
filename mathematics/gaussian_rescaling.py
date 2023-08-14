import cv2
import numpy as np

from mathematics.gaussian_smooth import gaussian_smooth


def gaussian_rescaling(img, scale_factor, sigma=1.0):
    if scale_factor < np.finfo(float).eps:
        print("Too small a scaling factor!!")
        return

    img_smooth = gaussian_smooth(img, 1.0 / scale_factor, 1e-3)
    img_scaled = cv2.resize(img_smooth, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)
    return img_scaled
