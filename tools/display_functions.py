import cv2
from tools.camera_integration import VideoCaptureDevice
from tools.image_filters import sobel_filter_gradient_magnitude


class LiveCapture(VideoCaptureDevice):
    def __init__(self, device_id=0, frame_height=720, frame_width=1280):
        super().__init__(device_id)
        self.__frame_height = frame_height
        self.__frame_width = frame_width

    def display_live_camera_signal_original(self, exit_key='q'):
        while True:
            cv2.imshow(
                "Live Camera",
                cv2.resize(
                    self.capture_frames(),
                    (self.__frame_width,
                     self.__frame_height)
                )
            )
            if cv2.waitKey(1) & 0xFF == ord(exit_key):
                raise SystemExit

    def display_live_camera_signal_sobel_filter_x(self, exit_key='q'):
        while True:
            cv2.imshow(
                "Live Camera Sobel X",
                cv2.resize(
                    cv2.Sobel(
                        self.capture_frames(),
                        cv2.CV_64F, 1, 0),
                    (self.__frame_width,
                     self.__frame_height)
                )
            )
            if cv2.waitKey(1) & 0xFF == ord(exit_key):
                raise SystemExit

    def display_live_camera_signal_sobel_filter_y(self, exit_key='q'):
        while True:
            cv2.imshow(
                "Live Camera Sobel Y",
                cv2.resize(
                    cv2.Sobel(
                        self.capture_frames(),
                        cv2.CV_64F, 0, 1
                    ),
                    (self.__frame_width,
                     self.__frame_height)
                )
            )
            if cv2.waitKey(1) & 0xFF == ord(exit_key):
                raise SystemExit

    def display_live_camera_signal_sobel_filter_magnitude(self, exit_key='q'):
        while True:
            cv2.imshow(
                "Live Camera Sobel Gradient Magnitude",
                cv2.resize(
                    sobel_filter_gradient_magnitude(
                        self.capture_frames()),
                    (self.__frame_width,
                     self.__frame_height)
                )
            )
            if cv2.waitKey(1) & 0xFF == ord(exit_key):
                raise SystemExit
