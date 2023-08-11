import numpy as np
from scipy.signal import convolve2d


def gaussian_smooth(img, sigma=1.0, endthresh=1e-9):
    max_mask_size = 100

    if sigma < 0.1:
        return img

    grid = np.linspace(-max_mask_size, max_mask_size, 2 * max_mask_size + 1)
    grid = 1.0 / (np.sqrt(2 * np.pi) * sigma) * np.exp(-grid ** 2 / (2 * sigma ** 2))
    lim = np.where(np.abs(grid) > np.abs(endthresh))[0]
    grid = grid[lim]
    grid = grid / np.sum(grid)

    if img.ndim == 3:
        img_smooth = img.copy()
        for i in range(3):
            img_smooth[:, :, i] = convolve2d(img[:, :, i], grid[:, np.newaxis], mode='same')
            img_smooth[:, :, i] = convolve2d(img_smooth[:, :, i], grid[np.newaxis, :], mode='same')
    else:
        img_smooth = convolve2d(img, grid[:, np.newaxis], mode='same')
        img_smooth = convolve2d(img_smooth, grid[np.newaxis, :], mode='same')

    return img_smooth
