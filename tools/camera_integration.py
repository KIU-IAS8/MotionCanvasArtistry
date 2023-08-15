import cv2


class VideoCaptureDevice:
    def __init__(self, device_id=0, width=800, height=800):
        self.video_capture = cv2.VideoCapture(device_id)
        self.__width = width,
        self.__height = height

    def capture_frame(self):
        if self.video_capture.isOpened():
            check, data = self.video_capture.read()
            if check:
                return self.resize(data, 2.3)
            else:
                raise Exception("Unable to extract frames")
        else:
            raise Exception("Video capture device is unavailable")

    def resize(self, data, scale):
        width = int(data.shape[1] * scale)
        height = int(data.shape[0] * scale)
        dim = (width, height)

        return cv2.resize(data, dim, interpolation=cv2.INTER_AREA)

