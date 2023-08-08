import cv2

from mathematics.optical_flow import optical_flow
from tools.display_functions import LiveCapture
from transformations.filters import sobel_filter_gradient_magnitude

lc = LiveCapture()

lc.display_sobel_filter_gradient_magnitude()


while True:
    frame1 = sobel_filter_gradient_magnitude(lc.capture_frames())
    frame2 = sobel_filter_gradient_magnitude(lc.capture_frames())
    cv2.imshow(
        "Live Camera Sobel Gradient Magnitude",
        cv2.resize(frame1, (1280, 720))
    )
    cv2.imshow(
        "Live Camera Sobel Gradient Magnitude",
        cv2.resize(frame2, (1280, 720))
    )

    optical_flow(frame1, frame2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        raise SystemExit
