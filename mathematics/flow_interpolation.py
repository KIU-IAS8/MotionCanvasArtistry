import numpy as np
import cv2


def optical_flow_interpolation(flow: np.ndarray, index: int) -> np.ndarray:
    h, w = flow.shape[:2]
    x, y = np.meshgrid(np.arange(w), np.arange(h))

    new_x = x + flow[..., 0]
    new_y = y + flow[..., 1]

    new_x = np.clip(new_x, 0, w - 1)
    new_y = np.clip(new_y, 0, h - 1)

    match index:
        case 1:
            interpolation = cv2.INTER_NEAREST
        case 2:
            interpolation = cv2.INTER_LINEAR
        case 3:
            interpolation = cv2.INTER_CUBIC
        case 4:
            interpolation = cv2.INTER_LANCZOS4
        case 5:
            interpolation = cv2.INTER_MAX
        case 6:
            interpolation = cv2.INTER_BITS
        case _:
            interpolation = cv2.INTER_CUBIC

    interpolated_flow = cv2.remap(
        flow,
        new_x.astype(np.float32),
        new_y.astype(np.float32),
        interpolation=interpolation
    )

    return interpolated_flow
