import cv2


class VideoCapture:
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

    def convert_to_grayscale(self):
        data = self.capture_frames()
        grayscale_data = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
        return grayscale_data

    def display_live_camera_signal(self, exit_key='q'):
        while True:
            cv2.imshow("Live Camera", self.capture_frames())
            if cv2.waitKey(1) & 0xFF == ord(exit_key):
                break
