def index_to_coordinate_mapper(i, factor, image_size):
    h = image_size // factor // 2
    index = i + factor
    step = factor * 2
    if index <= image_size // 2:
        k = (image_size // 2 + factor - index) // factor
        return (-image_size + ((h - k) * step) + factor) / image_size
    else:
        k = (-image_size // 2 + factor + index) // factor
        return (image_size - ((h - k) * step) - factor - step) / image_size


def coordinate_to_index_mapper(c, factor, image_size):
    c *= (image_size // 2)
    c += (image_size // 2)
    c -= (factor // 2)
    c = round(c)
    for x in range(1, factor):
        if (c + x) % factor == 0:
            c += x
    return c


def rotate_matrix_right(matrix):
    transposed = []
    for row in zip(*matrix):
        transposed.append(list(row))
    rotated = []
    for row in transposed:
        rotated.append(row[::-1])
    return rotated
