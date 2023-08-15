import cv2
import pytest
from tools.camera_integration import VideoCaptureDevice


class MockVideoCaptureDevice:
    def __init__(self, opened, frame_data=None):
        self.opened = opened
        self.frame_data = frame_data

    def read(self):
        return self.opened, self.frame_data

    def isOpened(self):
        return self.opened


@pytest.fixture
def mock_capture_device_opened():
    return MockVideoCaptureDevice(opened=True, frame_data=cv2.imread('../mock_data/images/img1.png'))


@pytest.fixture
def mock_capture_device_not_opened():
    return MockVideoCaptureDevice(opened=False)


def test_capture_frames_successful(mock_capture_device_opened):
    device = VideoCaptureDevice()
    device.video_capture = mock_capture_device_opened

    result_frame = device.capture_frame()

    assert (result_frame == mock_capture_device_opened.frame_data).all()


def test_capture_frames_device_unavailable(mock_capture_device_not_opened):
    device = VideoCaptureDevice(3)
    device.video_capture = mock_capture_device_not_opened

    with (pytest.raises(Exception)):
        device.capture_frame()
