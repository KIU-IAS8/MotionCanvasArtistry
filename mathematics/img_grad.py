import numpy as np
from scipy.signal import fftconvolve

from mathematics.gauss_deriv import gauss_deriv


def img_grad(I, sigma=1.0):
    if not isinstance(I, np.ndarray):
        I = np.array(I, dtype=float)

    gd = gauss_deriv(sigma)

    # Compute x and y derivatives using convolution
    xd = fftconvolve(I, gd[:, None, None], mode='same')
    yd = fftconvolve(I, gd[:, None, None], mode='same')

    return xd, yd
