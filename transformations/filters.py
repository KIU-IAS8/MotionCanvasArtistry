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
def scharr_filter_gradient_magnitude(image_matrix):

    gray_image = cv2.cvtColor(image_matrix, cv2.COLOR_BGR2GRAY)

    scharr_x = cv2.Scharr(gray_image, cv2.CV_64F, 1, 0)
    scharr_y = cv2.Scharr(gray_image, cv2.CV_64F, 0, 1)

    gradient_m = np.sqrt(scharr_x ** 2 + scharr_y ** 2)
    gradient_m = cv2.normalize(gradient_m, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

    return gradient_m

def prewitt_filter_gradient_magnitude(image_matrix):
    gray_image = cv2.cvtColor(image_matrix, cv2.COLOR_BGR2GRAY)

    prewitt_x = cv2.filter2D(gray_image, cv2.CV_64F, np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]))
    prewitt_y = cv2.filter2D(gray_image, cv2.CV_64F, np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]]))

    gradient_magnitude = np.sqrt(prewitt_x ** 2 + prewitt_y ** 2)
    gradient_magnitude = cv2.normalize(gradient_magnitude, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

    return gradient_magnitude

def canny_edge_detection(image_matrix):
    gray_image = cv2.cvtColor(image_matrix, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray_image, threshold1=100, threshold2=200)

    return edges

def roberts_cross_gradient_magnitude(image_matrix):
    gray_image = cv2.cvtColor(image_matrix, cv2.COLOR_BGR2GRAY)

    roberts_x = cv2.filter2D(gray_image, cv2.CV_64F, np.array([[1, 0], [0, -1]]))
    roberts_y = cv2.filter2D(gray_image, cv2.CV_64F, np.array([[0, 1], [-1, 0]]))

    gradient_magnitude = np.sqrt(roberts_x ** 2 + roberts_y ** 2)
    gradient_magnitude = cv2.normalize(gradient_magnitude, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

    return gradient_magnitude

def laplacian_filter_gradient_magnitude(image_matrix):
    gray_image = cv2.cvtColor(image_matrix, cv2.COLOR_BGR2GRAY)

    laplacian = cv2.Laplacian(gray_image, cv2.CV_64F)
    gradient_magnitude = np.abs(laplacian)
    gradient_magnitude = cv2.normalize(gradient_magnitude, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

    return gradient_magnitude