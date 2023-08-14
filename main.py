import random
from visualization.objects.sphere import Sphere
from visualization.visualize import Picture
from mathematics.operations import *
from vpython import vector
import cv2

factor = 10
width = 800
height = 800

image_path = "mock_data/images/img2.png"

picture = Picture(
    factor=factor,
    height=height,
    width=width,
    fps=30,
    scale=1.5,
    title=image_path
)

image = rotate_matrix_right(cv2.imread(image_path))

spheres = []

for x in range(0, len(image), factor):
    for y in range(0, len(image), factor):
        spheres.append(
            Sphere(
                picture=picture,
                position=vector(
                    index_to_coordinate_mapper(x, factor, len(image), width),
                    index_to_coordinate_mapper(y, factor, len(image), width),
                    0.0
                ),
                speed=(
                    random.uniform(-0.0025, 0.0025),
                    random.uniform(-0.0025, 0.0025),
                    0),
                rotation_angle_x=0.1,
                rotation_angle_y=0.0,
                # radius=1 / len(image) * factor + random.uniform(0, 0.001 * factor),
                radius=1 / len(image) * factor,
                color=vector(
                    image[x][y][2] / 255,
                    image[x][y][1] / 255,
                    image[x][y][0] / 255
                )
            )
        )

picture.visualize(spheres=spheres)
