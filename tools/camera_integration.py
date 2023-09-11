import cv2


class VideoCaptureDevice:
    def __init__(self, device_id=0):
        self.video_capture = cv2.VideoCapture(device_id)

    def capture_frame(self):
        if self.video_capture.isOpened():
            check, data = self.video_capture.read()
            if check:
                return cv2.rotate(cv2.flip(self.crop(data), 1), cv2.ROTATE_90_CLOCKWISE)
            else:
                raise Exception("Unable to extract frames")
        else:
            raise Exception("Video capture device is unavailable")

    def crop(self, data):
        return data[:, (data.shape[1] - data.shape[0]) // 2:(data.shape[1] - data.shape[0]) // 2 + data.shape[0], :]
