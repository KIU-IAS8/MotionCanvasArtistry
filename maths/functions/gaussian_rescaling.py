import cv2
import numpy as np
from scipy.ndimage import gaussian_filter


def gaussian_rescaling(img, scale_factor, sigma=1.0):
    if scale_factor < np.spacing(1.0):
        print("Too small a scaling factor!!")
        return

    h, w, c = img.shape
    img_smooth = gaussian_filter(img, sigma)
    img_scaled = cv2.resize(img_smooth, (int(w * scale_factor), int(h * scale_factor)))

    return img_scaled
