from __future__ import annotations
import numpy as np
from scipy.signal import convolve2d

HSKERN = np.array(
    [[1 / 12, 1 / 6, 1 / 12], [1 / 6, 0, 1 / 6], [1 / 12, 1 / 6, 1 / 12]], float
)

kernelX = np.array([[-1, 1], [-1, 1]]) * 0.25  # kernel for computing d/dx

kernelY = np.array([[-1, -1], [1, 1]]) * 0.25  # kernel for computing d/dy

kernelT = np.ones((2, 2)) * 0.25


def optical_flow_horn_schunck(im1: np.ndarray, im2: np.ndarray, *, alpha: float = 0.001, niter: int = 8) -> (
        tuple)[np.ndarray, np.ndarray]:

    im1 = im1.astype(np.float32)
    im2 = im2.astype(np.float32)

    u_initial = np.zeros([im1.shape[0], im1.shape[1]], dtype=np.float32)
    v_initial = np.zeros([im1.shape[0], im1.shape[1]], dtype=np.float32)

    u = u_initial
    v = v_initial

    [fx, fy, ft] = compute_derivatives(im1, im2)

    for _ in range(niter):
        u_avg = convolve2d(u, HSKERN, "same")
        v_avg = convolve2d(v, HSKERN, "same")

        der = (fx * u_avg + fy * v_avg + ft) / (alpha ** 2 + fx ** 2 + fy ** 2)

        u = u_avg - fx * der
        v = v_avg - fy * der

    return u.tolist(), v.tolist()


def compute_derivatives(im1: np.ndarray, im2: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    fx = convolve2d(im1, kernelX, "same") + convolve2d(im2, kernelX, "same")
    fy = convolve2d(im1, kernelY, "same") + convolve2d(im2, kernelY, "same")
    ft = convolve2d(im1, kernelT, "same") + convolve2d(im2, -kernelT, "same")

    return fx, fy, ft
