import cv2
import numpy as np
from constants.matrices import ONES


def sobel_filter_gradient_magnitude(image_matrix):
    gray_image = cv2.cvtColor(image_matrix, cv2.COLOR_BGR2GRAY)

    sobel_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)

    gradient_magnitude = np.sqrt(sobel_x ** 2 + sobel_y ** 2)
    gradient_magnitude = cv2.normalize(gradient_magnitude, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

    return gradient_magnitude


def morphological_filter(image_matrix):
    erosion = cv2.erode(image_matrix, np.array(ONES), iterations=1)
    dilation = cv2.dilate(image_matrix, np.array(ONES), iterations=1)

    return erosion, dilation
