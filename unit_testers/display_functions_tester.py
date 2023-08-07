import unittest
import cv2
from unittest.mock import Mock, patch
from tools.display_functions import LiveCapture


class TestLiveCapture(unittest.TestCase):
    def setUp(self):
        self.live_capture = LiveCapture()

    def tearDown(self):
        cv2.destroyAllWindows()

    def test_convert_to_grayscale(self):

        self.live_capture.capture_frames = Mock(return_value=cv2.imread('img1.png'))

        grayscale_data = self.live_capture.convert_to_grayscale()

        self.assertTrue(grayscale_data is not None)
        self.assertEqual(grayscale_data.shape[-1], 1)  # Check if the image is grayscale

    def test_display_live_camera_signal_original(self):
        with patch('cv2.imshow') as mock_imshow, patch('cv2.waitKey') as mock_waitkey:
            mock_waitkey.return_value = ord('q')

            self.live_capture.display_live_camera_signal_original()

            mock_imshow.assert_called_with('Live Camera', cv2.resize.return_value)

    def test_display_live_camera_signal_sobel_filter_x(self):
        with patch('cv2.imshow') as mock_imshow, patch('cv2.waitKey') as mock_waitkey, \
             patch('cv2.Sobel') as mock_sobel:
            mock_waitkey.return_value = ord('q')
            mock_sobel.return_value = cv2.imread('img1.png')

            self.live_capture.display_live_camera_signal_sobel_filter_x()

            mock_imshow.assert_called_with('Live Camera Sobel X', cv2.resize.return_value)

    def test_display_live_camera_signal_sobel_filter_y(self):
        with patch('cv2.imshow') as mock_imshow, patch('cv2.waitKey') as mock_waitkey, \
             patch('cv2.Sobel') as mock_sobel:
            mock_waitkey.return_value = ord('q')
            mock_sobel.return_value = cv2.imread('sample_image.jpg')

            self.live_capture.display_live_camera_signal_sobel_filter_y()

            mock_imshow.assert_called_with('Live Camera Sobel Y', cv2.resize.return_value)

    def test_display_live_camera_signal_sobel_filter_magnitude(self):
        with patch('cv2.imshow') as mock_imshow, patch('cv2.waitKey') as mock_waitkey, \
             patch('sobel_filter_gradient_magnitude') as mock_sobel_filter:
            mock_waitkey.return_value = ord('q')
            mock_sobel_filter.return_value = cv2.imread('sample_image.jpg')

            self.live_capture.display_live_camera_signal_sobel_filter_magnitude()

            mock_imshow.assert_called_with('Live Camera Sobel Gradient Magnitude', cv2.resize.return_value)


if __name__ == '__main__':
    unittest.main()