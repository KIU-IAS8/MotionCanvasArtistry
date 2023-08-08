import cv2
from tools.camera_integration import VideoCaptureDevice
from tools.image_filters import sobel_filter_gradient_magnitude, morphological_filter


class LiveCapture(VideoCaptureDevice):
    def __init__(self, device_id=0, frame_height=720, frame_width=1280, exit_key='q'):
        super().__init__(device_id)
        self.__frame_height = frame_height
        self.__frame_width = frame_width
        self.__exit_key = exit_key

    def convert_to_grayscale(self):
        data = self.capture_frames()
        grayscale_data = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
        return grayscale_data

    def display_signal_original(self):
        while True:
            cv2.imshow(
                "Live Camera",
                cv2.resize(
                    self.capture_frames(),
                    (self.__frame_width,
                     self.__frame_height)
                )
            )
            if cv2.waitKey(1) & 0xFF == ord(self.__exit_key):
                raise SystemExit

    def display_sobel_filter_x(self):
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
            if cv2.waitKey(1) & 0xFF == ord(self.__exit_key):
                raise SystemExit

    def display_sobel_filter_y(self):
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
            if cv2.waitKey(1) & 0xFF == ord(self.__exit_key):
                raise SystemExit

    def display_sobel_filter_gradient_magnitude(self):
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
            if cv2.waitKey(1) & 0xFF == ord(self.__exit_key):
                raise SystemExit

    def display_morphological_filter_erosion(self):
        while True:
            cv2.imshow(
                "Live Camera Morphological Erosion",
                cv2.resize(
                    morphological_filter(
                        self.capture_frames())[0],
                    (self.__frame_width,
                     self.__frame_height)
                )
            )
            if cv2.waitKey(1) & 0xFF == ord(self.__exit_key):
                raise SystemExit

    def display_morphological_filter_dilation(self):
        while True:
            cv2.imshow(
                "Live Camera Morphological Dilation",
                cv2.resize(
                    morphological_filter(
                        self.capture_frames())[1],
                    (self.__frame_width,
                     self.__frame_height)
                )
            )
            if cv2.waitKey(1) & 0xFF == ord(self.__exit_key):
                raise SystemExit

    def display_morphological_filter_erosion_sobel_gradient_magnitude(self):
        while True:
            cv2.imshow(
                "Live Camera Morphological Erosion On Sobel Gradient Magnitude",
                cv2.resize(
                    morphological_filter(
                        sobel_filter_gradient_magnitude(self.capture_frames()))[0],
                    (self.__frame_width,
                     self.__frame_height)
                )
            )
            if cv2.waitKey(1) & 0xFF == ord(self.__exit_key):
                raise SystemExit

    def display_morphological_filter_dilation_sobel_gradient_magnitude(self):
        while True:
            cv2.imshow(
                "Live Camera Morphological Dilation On Sobel Gradient Magnitude",
                cv2.resize(
                    morphological_filter(
                        sobel_filter_gradient_magnitude(self.capture_frames()))[1],
                    (self.__frame_width,
                     self.__frame_height)
                )
            )
            if cv2.waitKey(1) & 0xFF == ord(self.__exit_key):
                raise SystemExit
