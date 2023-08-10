from tools.display_functions import LiveCapture
from visualization.objects.sphere import Sphere
from visualization.visualize import Picture
from mathematics.operations import *
import cv2

# lc = LiveCapture()
# lc.display_sobel_filter_gradient_magnitude()

picture = Picture(factor=50, height=1000, width=1000)

image = rotate_matrix_right(cv2.imread("mock_data/images/img2.png"))

spheres = []

for x in range(0, len(image), picture.get_factor()):
    for y in range(0, len(image), picture.get_factor()):
        spheres.append(
            Sphere(radius=1 / len(image) * picture.get_factor(),
                   position=(
                       index_to_coordinate_mapper(x, picture.get_factor(), len(image), picture.get_width()),
                       index_to_coordinate_mapper(y, picture.get_factor(), len(image), picture.get_width()),
                       0.0
                   ),
                   start_color=(image[x][y][2] / 255 - 0.1, image[x][y][1] / 255 - 0.1, image[x][y][0] / 255 - 0.1),
                   end_color=(image[x][y][2] / 255 + 0.1, image[x][y][1] / 255 + 0.1, image[x][y][0] / 255 + 0.1),
                   speed=(0.000, 0.000, 0.0),
                   slices=3,
                   stacks=10,
                   rotation_angle=45,
                   rotation_speed=10)
        )
        print(x, y)

# s1 = Sphere(radius=0.01, position=(900 / 1000, 900 / 1000, 0.0), start_color=image[800][10], end_color=image[800][0],
#             speed=(0.000, 0.000, 0.0), slices=3, stacks=3, rotation_angle=45, rotation_speed=10)

picture.visualize(spheres=spheres)
