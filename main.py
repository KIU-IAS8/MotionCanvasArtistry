from tools.camera_functions import VideoCapture


vc = VideoCapture()

# vc.display_live_camera_signal_original()
# vc.display_live_camera_signal_sobel_filter_x()
# vc.display_live_camera_signal_sobel_filter_y()

vc.display_live_camera_signal_sobel_filter_magnitude()
