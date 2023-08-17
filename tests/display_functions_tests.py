import cv2
import unittest
from unittest.mock import MagicMock
from tools.display_functions import LiveCapture


class TestLiveCapture(unittest.TestCase):
    def setUp(self):
        self.mock_capture_device = MagicMock()

    def test_display_live_camera_signal_original(self):
        self.mock_capture_device.capture_frames.return_value = cv2.imread('../mock_data/images/img1.png')
        live_capture = LiveCapture()
        live_capture.capture_frame = self.mock_capture_device.capture_frames

        with self.assertRaises(SystemExit):
            live_capture.display_live_camera_signal_original('q')

    def test_display_live_camera_signal_sobel_filter_x(self):
        self.mock_capture_device.capture_frames.return_value = cv2.imread('../mock_data/images/img1.png')
        live_capture = LiveCapture()
        live_capture.capture_frame = self.mock_capture_device.capture_frames

        with self.assertRaises(SystemExit):
            live_capture.display_live_camera_signal_sobel_filter_x('q')

    def test_display_live_camera_signal_sobel_filter_y(self):
        self.mock_capture_device.capture_frames.return_value = cv2.imread('../mock_data/images/img1.png')
        live_capture = LiveCapture()
        live_capture.capture_frame = self.mock_capture_device.capture_frames

        with self.assertRaises(SystemExit):
            live_capture.display_live_camera_signal_sobel_filter_y('q')

    def test_display_live_camera_signal_sobel_filter_gradient_magnitude(self):
        self.mock_capture_device.capture_frames.return_value = cv2.imread('../mock_data/images/img1.png')
        live_capture = LiveCapture()
        live_capture.capture_frame = self.mock_capture_device.capture_frames

        with self.assertRaises(SystemExit):
            live_capture.display_live_camera_signal_sobel_filter_magnitude('q')
