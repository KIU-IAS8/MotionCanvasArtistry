import cv2


def convert_to_grayscale(image):
    return [[sum(pixel[:3]) / 3 for pixel in row] for row in image]


def convert_to_grayscale_cv2(image):
    grayscale_data = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return grayscale_data
