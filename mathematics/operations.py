def index_to_coordinate_mapper(i, factor, image_size, window_size):
    c = window_size / image_size
    h = image_size // factor // 2
    index = i + factor
    step = factor * 2
    if index <= image_size // 2:
        k = (image_size // 2 + factor - index) // factor
        return (-image_size + ((h - k) * step) + factor) / image_size
    else:
        k = (-image_size // 2 + factor + index) // factor
        return (image_size - ((h - k) * step) - factor - step) / image_size


def rotate_matrix_right(matrix):
    transposed = []
    for row in zip(*matrix):
        transposed.append(list(row))
    rotated = []
    for row in transposed:
        rotated.append(row[::-1])
    return rotated
