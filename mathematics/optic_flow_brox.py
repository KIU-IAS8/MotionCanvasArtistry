import numpy as np
import cv2
import matplotlib.pyplot as plt

from mathematics.mywarp_rgb import mywarp_rgb


def optic_flow_brox(img1, img2):
    alpha = 30.0
    gamma = 80.0
    ht, wt, dt = img1.shape
    num_levels = 40
    im1_hr = gaussian_rescaling(img1, np.power(0.95, num_levels))
    im2_hr = gaussian_rescaling(img2, np.power(0.95, num_levels))
    u = np.zeros(im1_hr[:, :, 0].shape)
    v = np.zeros(im1_hr[:, :, 0].shape)
    for i in range(num_levels - 1, 0, -1):
        I1 = cv2.cvtColor(im1_hr, cv2.COLOR_RGB2GRAY)
        I2 = cv2.cvtColor(im2_hr, cv2.COLOR_RGB2GRAY)

        Ikx, Iky = img_grad(I2)
        Ikx2, Iky2 = img_grad(I1)
        Ikz = np.double(I2) - np.double(I1)
        Ixz = np.double(Ikx) - np.double(Ikx2)
        Iyz = np.double(Iky) - np.double(Iky2)

        du, dv = resolution_process_brox(Ikz, Ikx, Iky, Ixz, Iyz, alpha, gamma, 1.8, u, v, 3, 500)

        u = u + du
        v = v + dv
        im1_hr = gaussian_rescaling(img1, np.power(0.95, i))
        im2_hr = gaussian_rescaling(img2, np.power(0.95, i))
        im2_orig = im2_hr
        u = cv2.resize(u, (im1_hr.shape[1], im1_hr.shape[0]), interpolation=cv2.INTER_LINEAR)
        v = cv2.resize(v, (im1_hr.shape[1], im1_hr.shape[0]), interpolation=cv2.INTER_LINEAR)
        im2_hr = mywarp_rgb(np.double(im2_hr), u, v)

        plt.figure(2)
        plt.subplot(3, 3, 1)
        plt.imshow(im1_hr)
        plt.subplot(3, 3, 2)
        plt.imshow(cv2.cvtColor(im2_hr, cv2.COLOR_RGB2GRAY))
        plt.subplot(3, 3, 3)
        plt.imshow(cv2.cvtColor(im2_orig, cv2.COLOR_RGB2GRAY))
        plt.subplot(3, 3, 4)
        plt.imshow(np.uint8(np.double(im1_hr) - np.double(im2_hr)))
        plt.subplot(3, 3, 5)
        plt.imshow(np.uint8(np.double(im1_hr) - np.double(im2_orig)))
        plt.subplot(3, 3, 6)
        plt.imshow(np.uint8(np.double(im2_hr) - np.double(im2_orig)))
        plt.subplot(3, 3, 7)
        plt.imshow(u)
        plt.subplot(3, 3, 8)
        plt.imshow(v)
        plt.subplot(3, 3, 9)
        plt.imshow(np.sqrt(u ** 2 + v ** 2))
        plt.show()
