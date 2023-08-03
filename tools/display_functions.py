import cv2
from tools.camera_integration import VideoCaptureDevice
from maths.functions.filters import sobel_filter_gradient_magnitude


class VideoCapture(VideoCaptureDevice):
    def __init__(self, device_id=0):
        super().__init__(device_id)

    def convert_to_grayscale(self):
        data = self.capture_frames()
        grayscale_data = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
        return grayscale_data

    def display_live_camera_signal_original(self, exit_key='q'):
        while True:
            cv2.imshow("Live Camera", self.capture_frames())
            if cv2.waitKey(1) & 0xFF == ord(exit_key):
                break

    def display_live_camera_signal_sobel_filter_x(self, exit_key='q'):
        while True:
            cv2.imshow("Live Camera Sobel X", cv2.Sobel(self.capture_frames(), cv2.CV_64F, 1, 0))
            if cv2.waitKey(1) & 0xFF == ord(exit_key):
                break

    def display_live_camera_signal_sobel_filter_y(self, exit_key='q'):
        while True:
            cv2.imshow("Live Camera Sobel X", cv2.Sobel(self.capture_frames(), cv2.CV_64F, 0, 1))
            if cv2.waitKey(1) & 0xFF == ord(exit_key):
                break

    def display_live_camera_signal_sobel_filter_magnitude(self, exit_key='q'):
        while True:
            cv2.imshow("Live Camera Sobel Gradient Magnitude", sobel_filter_gradient_magnitude(self.capture_frames()))
            if cv2.waitKey(1) & 0xFF == ord(exit_key):
                break
