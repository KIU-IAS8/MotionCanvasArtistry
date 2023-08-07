import unittest
from unittest.mock import Mock, patch
from tools.camera_integration import VideoCaptureDevice


class TestVideoCaptureDevice(unittest.TestCase):
    def setUp(self):
        self.device_id = 0
        self.video_capture = VideoCaptureDevice(self.device_id)

    def test_capture_frames_success(self):
        mock_read = Mock(return_value=(True, 'sample_data'))

        with patch('cv2.VideoCapture', return_value=Mock(read=mock_read)) as mock_cv2_capture:
            result = self.video_capture.capture_frames()

            mock_cv2_capture.assert_called_once_with(self.device_id)
            mock_read.assert_called_once()

            self.assertEqual(result, 'sample_data')

    def test_capture_frames_failure(self):
        mock_read = Mock(return_value=(False, None))

        with patch('cv2.VideoCapture', return_value=Mock(read=mock_read)) as mock_cv2_capture:
            with self.assertRaises(Exception) as context:
                self.video_capture.capture_frames()

            mock_cv2_capture.assert_called_once_with(self.device_id)
            mock_read.assert_called_once()

            self.assertEqual(str(context.exception), "Unable to extract frames")

    def test_capture_frames_device_unavailable(self):
        with patch('cv2.VideoCapture', return_value=Mock(isOpened=Mock(return_value=False))):
            with self.assertRaises(Exception) as context:
                self.video_capture.capture_frames()

            self.assertEqual(str(context.exception), "Video capture device is unavailable")


if __name__ == '__main__':
    unittest.main()