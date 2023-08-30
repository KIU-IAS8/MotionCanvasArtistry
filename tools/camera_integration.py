import cv2


class VideoCaptureDevice:
    def __init__(self, device_id=0, width=360, height=360):
        self.video_capture = cv2.VideoCapture(device_id)
        self.__width = width
        self.__height = height

    def capture_frame(self):
        if self.video_capture.isOpened():
            check, data = self.video_capture.read()
            if check:
                return cv2.flip(self.crop(data), 1)
            else:
                raise Exception("Unable to extract frames")
        else:
            raise Exception("Video capture device is unavailable")

    def crop(self, data):
        return data[:, (data.shape[1] - self.__width) // 2:(data.shape[1] - self.__width) // 2 + self.__width, :]