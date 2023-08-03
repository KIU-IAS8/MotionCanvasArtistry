def convert_to_grayscale(image):
    return [[sum(pixel[:3]) / 3 for pixel in row] for row in image]
