import numpy as np


def sobel_filter(**kwargs):
    filter_matrix = np.array(kwargs["filter"])
    frame = np.array(kwargs["frame"], dtype=np.uint8)

    padding = kwargs["padding"]
    strides = kwargs["strides"]

    kernel = np.flipud(np.fliplr(filter_matrix))

    kernel_shape_x = kernel.shape[0]
    kernel_shape_y = kernel.shape[1]

    frame_shape_x = frame.shape[0]
    frame_shape_y = frame.shape[1]

    output_x = int(((frame_shape_x - kernel_shape_x + 2 * padding) / strides))
    output_y = int(((frame_shape_y - kernel_shape_y + 2 * padding) / strides))

    output = np.zeros((output_x, output_y))

    if padding != 0:
        padded_frame = np.zeros((frame.shape[0] + padding * 2, frame.shape[1] + padding * 2))
        padded_frame[int(padding):int(-1 * padding), int(padding):int(-1 * padding)] = frame
    else:
        padded_frame = frame

    for y in range(frame.shape[1]):
        if y > frame.shape[1] - kernel_shape_y:
            break
        if y % strides == 0:
            for x in range(frame.shape[0]):
                if x > frame.shape[0] - kernel_shape_x:
                    break

                try:
                    if x % strides == 0:
                        output[x, y] = (kernel * padded_frame[x: x + kernel_shape_x, y: y + kernel_shape_y]).sum()
                except IndexError:
                    break

    return output
