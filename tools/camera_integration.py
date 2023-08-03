import cv2


class VideoCaptureDevice:
    def __init__(self, device_id=0):
        self.device_id = device_id
        self.video_capture = cv2.VideoCapture(device_id)

    def capture_frames(self):
        if self.video_capture.isOpened():
            check, data = self.video_capture.read()
            if check:
                return data
            else:
                raise Exception("Unable to extract frames")
        else:
            raise Exception("Video capture device is unavailable")


