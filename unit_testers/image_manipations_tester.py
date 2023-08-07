import unittest
from tools.image_manipulations import convert_to_grayscale


class TestConvertToGrayscale(unittest.TestCase):
    def test_convert_to_grayscale(self):

        sample_image = [
            [(255, 0, 0), (0, 255, 0), (0, 0, 255)],
            [(128, 128, 128), (64, 64, 64), (192, 192, 192)],
            [(0, 0, 0), (255, 255, 255), (128, 128, 128)]
        ]

        expected_result = [
            [85, 85, 85],
            [128, 64, 128],
            [0, 255, 128]
        ]

        result = convert_to_grayscale(sample_image)

        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
