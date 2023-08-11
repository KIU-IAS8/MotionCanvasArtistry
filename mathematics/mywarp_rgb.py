import numpy as np
from scipy.interpolate import interp2d


def mywarp_rgb(im1, u, v):
    h, w, d = im1.shape
    uc, vc = np.meshgrid(np.arange(1, w + 1), np.arange(1, h + 1))
    uc1 = uc + u
    vc1 = vc + v
    warpedim = np.zeros_like(im1)

    for channel in range(d):
        f = interp2d(uc[0], vc[:, 0], im1[:, :, channel], kind='linear', fill_value=0)
        warpedim[:, :, channel] = f(uc1[0], vc1[:, 0])

    return warpedim
