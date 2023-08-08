import math

import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import interp2d
from skimage.util import img_as_ubyte

from mathematics.gaussian_rescaling import gaussian_rescaling_func
from skimage.transform import resize
from scipy.sparse import csr_matrix


def optical_flow(img1, img2):
    alpha = 30
    gamma = 80

    ht, wt, dt = img1.shape

    num_levels = 40

    im1_hr = gaussian_rescaling_func(img1, pow(0.95, num_levels))
    im2_hr = gaussian_rescaling_func(img2, pow(0.95, num_levels))

    u = np.zeros(cv2.cvtColor(im1_hr, cv2.COLOR_BGR2GRAY).shape)
    v = np.zeros(cv2.cvtColor(im1_hr, cv2.COLOR_BGR2GRAY).shape)

    for i in range(num_levels-2, 0, -1):
        I1 = cv2.cvtColor(im1_hr, cv2.COLOR_BGR2GRAY)
        I2 = cv2.cvtColor(im2_hr, cv2.COLOR_BGR2GRAY)

        Ikx, Iky = np.gradient(I2)
        Ikx2, Iky2 = np.gradient(I1)
        Ikz = I2 - I1
        Ixz = Ikx - Ikx2
        Iyz = Iky - Iky2

        Ixx, Ixy = np.gradient(Ikx)
        Iyx, Iyy = np.gradient(Iky)

        du = np.zeros((ht, wt))
        dv = np.zeros((ht, wt))
        tol = 1e-8 * np.ones((2 * ht * wt, 1))
        duv = np.zeros((2 * ht * wt, 1))

        for j in range(0, 3):
            term1 = (Ikz + Ikx * du + Iky * dv) ** 2
            term2 = (Ixz + Ixx * du + Ixy * dv) ** 2
            term3 = (Iyz + Ixy * du + Iyy * dv) ** 2
            arg = term1 + gamma * (term2 + term3)
            psidash = psi_derivative(arg)

            psidashFS = PsidashFS_brox(u + du, v + dv)
            A, b = constructMatrix(Ikx, Iky, Ikz, Ixx, Ixy, Iyy, Ixz, Iyz, psidash, alpha * psidashFS, u, v, gamma)

            duv, err, it, flag = sor(A, duv, b, 1.8, 500, tol)

            du = duv[::2].reshape((ht, wt))
            dv = duv[1::2].reshape((ht, wt))

            u = u + du
            v = v + dv
            im1_hr = gaussian_rescaling_func(img1, math.pow(0.95, i))
            im2_hr = gaussian_rescaling_func(img2, math.pow(0.95, i))
            im2_orig = im2_hr

            u_resized = resize(u, (im1_hr.shape[0], im1_hr.shape[1]), order=1, mode='reflect', anti_aliasing=True)
            v_resized = resize(v, (im1_hr.shape[0], im1_hr.shape[1]), order=1, mode='reflect', anti_aliasing=True)
            im2_hr = img_as_ubyte(mywarp_rgb(im2_hr.astype(float), u, v))

            fig = plt.figure(figsize=(12, 10))

            # Plotting the subplots
            plt.subplot(3, 3, 1)
            plt.imshow(im1_hr)
            plt.title("im1_hr")

            plt.subplot(3, 3, 2)
            plt.imshow(cv2.cvtColor(im2_hr, cv2.COLOR_BGR2GRAY), cmap='gray')
            plt.title("rgb2gray(im2_hr)")

            plt.subplot(3, 3, 3)
            plt.imshow(cv2.cvtColor(im2_orig, cv2.COLOR_BGR2GRAY), cmap='gray')
            plt.title("rgb2gray(im2_orig)")

            plt.subplot(3, 3, 4)
            plt.imshow(np.uint8(np.double(im1_hr) - np.double(im2_hr)))
            plt.title("im1_hr - im2_hr")

            plt.subplot(3, 3, 5)
            plt.imshow(np.uint8(np.double(im1_hr) - np.double(im2_orig)))
            plt.title("im1_hr - im2_orig")

            plt.subplot(3, 3, 6)
            plt.imshow(np.uint8(np.double(im2_hr) - np.double(im2_orig)))
            plt.title("im2_hr - im2_orig")

            plt.subplot(3, 3, 7)
            plt.imshow(u, cmap='jet')
            plt.title("u")

            plt.subplot(3, 3, 8)
            plt.imshow(v, cmap='jet')
            plt.title("v")

            plt.subplot(3, 3, 9)
            plt.imshow(np.sqrt(u ** 2 + v ** 2), cmap='jet')
            plt.title("sqrt(u^2 + v^2)")

            plt.tight_layout()
            plt.show()


def psi_derivative(x, epsilon=1e-3):
    return 1 / (2 * math.sqrt(x + epsilon))


def PsidashFS_brox(u, v):
    h, w = u.shape
    psidashFS = np.zeros((2 * h + 1, 2 * w + 1))

    ux = np.convolve(u, [1, -1], mode='same')
    uy = np.convolve(u, [1, -1], mode='same')
    vx = np.convolve(v, [1, -1], mode='same')
    vy = np.convolve(v, [1, -1], mode='same')

    uxd = np.convolve(ux, [0.5, 0.5], mode='valid')
    vxd = np.convolve(vx, [0.5, 0.5], mode='valid')
    uyd = np.convolve(uy, [0.5, 0.5], mode='valid')
    vyd = np.convolve(vy, [0.5, 0.5], mode='valid')

    t = np.convolve(uyd, [0.5, 0.5])
    uypd = uy ** 2 + t ** 2

    t = np.convolve(uxd, [0.5, 0.5])
    uxpd = ux ** 2 + t ** 2

    t = np.convolve(vyd, [0.5, 0.5])
    vypd = vy ** 2 + t ** 2

    t = np.convolve(vxd, [0.5, 0.5])
    vxpd = vx ** 2 + t ** 2

    psidashFS[::2, 1::2] = psi_derivative(uypd + vypd)
    psidashFS[1::2, ::2] = psi_derivative(uxpd + vxpd)

    return psidashFS


def constructMatrix(Ikx, Iky, Ikz, Ixx, Ixy, Iyy, Ixz, Iyz, pd, pdfs, u, v, gamma):
    ht, wt = u.shape

    pdfs[0, :] = 0
    pdfs[:, 0] = 0
    pdfs[-1, :] = 0
    pdfs[:, -1] = 0

    tmp = np.arange(1, 2 * ht * wt + 1).reshape(6, -1, order='F')
    rs = tmp.ravel()
    cs = rs.copy()
    ss = np.zeros_like(rs)

    cs[0::6] = rs[0::6] - 2 * ht
    cs[1::6] = rs[1::6] - 2
    cs[8::12] = rs[8::12] - 1
    cs[3::12] = rs[3::12] + 1
    cs[4::6] = rs[4::6] + 2
    cs[5::6] = rs[5::6] + 2 * ht

    pdfsum = pdfs[0::2, 1::2] + pdfs[2::2, 1::2] + pdfs[1::2, 0::2] + pdfs[1::2, 2::2]

    uapp = pd * (Ikx ** 2 + gamma * (Ixx ** 2 + Ixy ** 2)) + pdfsum
    vapp = pd * (Iky ** 2 + gamma * (Iyy ** 2 + Ixy ** 2)) + pdfsum
    uvapp = pd * (Ikx * Iky + gamma * (Ixx * Ixy + Iyy * Ixy))
    vuapp = pd * (Ikx * Iky + gamma * (Ixx * Ixy + Iyy * Ixy))

    ss[2::12] = uapp
    ss[9::12] = vapp
    ss[3::12] = uvapp
    ss[8::12] = vuapp

    tmp = pdfs[1::2, 0::2]
    ss[0::12] = -tmp.ravel()
    ss[6::12] = -tmp.ravel()

    tmp = pdfs[1::2, 2::2]
    ss[5::12] = -tmp.ravel()
    ss[11::12] = -tmp.ravel()

    tmp = pdfs[0::2, 1::2]
    ss[1::12] = -tmp.ravel()
    ss[7::12] = -tmp.ravel()

    tmp = pdfs[2::2, 1::2]
    ss[4::12] = -tmp.ravel()
    ss[10::12] = -tmp.ravel()

    upad = np.pad(u, [(1, 1), (1, 1)], mode='constant')
    vpad = np.pad(v, [(1, 1), (1, 1)], mode='constant')

    pdfaltsumu = (pdfs[1::2, 0::2] * (upad[1:ht+1, :wt] - upad[1:ht+1, 1:wt+1]) +
                  pdfs[1::2, 2::2] * (upad[1:ht+1, 2:] - upad[1:ht+1, 1:wt+1]) +
                  pdfs[0::2, 1::2] * (upad[:ht, 1:wt+1] - upad[1:ht+1, 1:wt+1]) +
                  pdfs[2::2, 1::2] * (upad[2:, 1:wt+1] - upad[1:ht+1, 1:wt+1]))

    pdfaltsumv = (pdfs[1::2, 0::2] * (vpad[1:ht+1, :wt] - vpad[1:ht+1, 1:wt+1]) +
                  pdfs[1::2, 2::2] * (vpad[1:ht+1, 2:] - vpad[1:ht+1, 1:wt+1]) +
                  pdfs[0::2, 1::2] * (vpad[:ht, 1:wt+1] - vpad[1:ht+1, 1:wt+1]) +
                  pdfs[2::2, 1::2] * (vpad[2:, 1:wt+1] - vpad[1:ht+1, 1:wt+1]))

    constu = pd * (Ikx * Ikz + gamma * (Ixx * Ixz + Ixy * Iyz)) - pdfaltsumu
    constv = pd * (Iky * Ikz + gamma * (Ixy * Ixz + Iyy * Iyz)) - pdfaltsumv

    b = np.zeros(2 * ht * wt)
    b[0::2] = -constu.ravel()
    b[1::2] = -constv.ravel()

    ind = np.where((cs > 0) & (cs < (2 * ht * wt + 1)))
    rs = rs[ind]
    cs = cs[ind]
    ss = ss[ind]

    A = csr_matrix((ss, (rs - 1, cs - 1)), shape=(2 * ht * wt, 2 * ht * wt))

    return A, b


def split(A, b, w, flag):
    m, n = A.shape

    if flag == 1:  # jacobi splitting
        M = np.diag(np.diag(A))
        N = np.diag(np.diag(A)) - A
    elif flag == 2:  # sor/gauss-seidel splitting
        b = w * b
        M = w * np.tril(A, -1) + np.diag(np.diag(A))
        N = -w * np.triu(A, 1) + (1.0 - w) * np.diag(np.diag(A))

    return M, N, b


def sor(A, x, b, w, max_it, tol):
    flag = 0  # initialization
    iter = 0
    bnrm2 = np.linalg.norm(b)
    if bnrm2 == 0.0:
        bnrm2 = 1.0
    r = b - A @ x
    error = np.linalg.norm(r) / bnrm2
    if error < tol:
        return x, error, iter, flag

    M, N, b = split(A, b, w, 2)  # matrix splitting (implementation of split required)
    for iter in range(1, max_it + 1):
        x_1 = x.copy()
        x = np.linalg.solve(M, N @ x + b)  # update approximation
        error = np.linalg.norm(x - x_1) / np.linalg.norm(x)  # compute error
        if error <= tol:
            break

    b = b / w  # restore rhs
    r = b - A @ x
    print(np.sum(np.abs(r)))
    print(np.max(np.abs(x)))
    if error > tol:
        flag = 1

    return x, error, iter, flag


def mywarp_rgb(im1, u, v):
    h, w, d = im1.shape
    uc, vc = np.meshgrid(np.arange(1, w + 1), np.arange(1, h + 1))
    uc1 = uc + u
    vc1 = vc + v
    warpedim = np.zeros_like(im1)

    for channel in range(d):
        interpolator = interp2d(uc[0], vc[:, 0], im1[:, :, channel], kind='linear', bounds_error=False)
        warpedim[:, :, channel] = interpolator(uc1.ravel(), vc1.ravel()).reshape((h, w))

    return warpedim
