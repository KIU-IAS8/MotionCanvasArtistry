import unittest
import cv2
import numpy as np
from unittest.mock import patch
from tools.image_filters import sobel_filter_gradient_magnitude


class TestSobelFilterGradientMagnitude(unittest.TestCase):
    def setUp(self):
        self.sample_image = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)

    def test_sobel_filter_gradient_magnitude(self):
        with patch('cv2.Sobel') as mock_sobel, patch('cv2.cvtColor') as mock_cvtColor, \
             patch('cv2.normalize') as mock_normalize:
            mock_sobel.side_effect = lambda img, dtype, dx, dy, ksize: img * 2  # Mock Sobel results
            mock_cvtColor.return_value = self.sample_image
            mock_normalize.return_value = self.sample_image

            result = sobel_filter_gradient_magnitude(self.sample_image)

            mock_cvtColor.assert_called_once_with(self.sample_image, cv2.COLOR_BGR2GRAY)
            mock_sobel.assert_any_call(mock_cvtColor.return_value, cv2.CV_64F, 1, 0, ksize=3)
            mock_sobel.assert_any_call(mock_cvtColor.return_value, cv2.CV_64F, 0, 1, ksize=3)
            mock_normalize.assert_called_once_with(
                np.sqrt(mock_sobel.return_value ** 2 + mock_sobel.return_value ** 2),
                None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U
            )

            self.assertTrue(np.array_equal(result, mock_normalize.return_value))


if __name__ == '__main__':
    unittest.main()