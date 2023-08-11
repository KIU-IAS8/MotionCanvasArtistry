import numpy as np


def gauss_deriv(sigma, thresh=1e-6):
    max_limit = 10000
    x = np.linspace(-max_limit, max_limit, 2 * max_limit + 1)
    variance = sigma ** 2
    numer = x ** 2
    denom = 2 * variance
    gd = np.exp(-numer / denom) / (np.pi * denom) ** 0.5
    gd = -gd * (x / variance)
    gd = gd[np.abs(gd) > thresh]  # cropping the filter
    return gd
