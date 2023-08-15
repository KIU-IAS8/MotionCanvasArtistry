from tools.camera_integration import VideoCaptureDevice
from transformations.conversions import convert_to_grayscale_cv2
from visualization.objects.sphere import Sphere
from visualization.visualize import Picture
from mathematics.operations import rotate_matrix_right, index_to_coordinate_mapper
from mathematics.optical_flow import optical_flow_horn_schunck
from vpython import vector, rate
import time
import cv2


def initialize(factor=10, width=800, height=800, image_path="mock_data/images/img2.png"):
    camera = VideoCaptureDevice()
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
                        index_to_coordinate_mapper(y, factor, len(image), height),
                        0.0
                    ),
                    rotation_angle_x=0.1,
                    rotation_angle_y=0.0,
                    radius=1 / len(image) * factor,
                    color=vector(
                        image[x][y][2] / 255,
                        image[x][y][1] / 255,
                        image[x][y][0] / 255
                    )
                )
            )

    return camera, picture, image, spheres


def main(factor=20, width=800, height=800, image_path="mock_data/images/img2.png"):
    camera, picture, image, spheres = initialize(factor=factor, width=width, height=height, image_path=image_path)

    picture.visualize(spheres=spheres)
    time.sleep(1)

    frame1 = convert_to_grayscale_cv2(camera.capture_frame())

    while True:
        rate(picture.get_rate())

        frame2 = convert_to_grayscale_cv2(camera.capture_frame())
        u, v = optical_flow_horn_schunck(frame1, frame2)

        accelerations = []

        for i in range((len(u) - height) // 2, (len(u) + height) // 2, factor):
            for j in range((len(u[i]) - width) // 2, (len(u[i]) + width) // 2, factor):
                accelerations.append([round(float(u[i][j]) / 10, 5), round(float(v[i][j]) / 10, 5)])

        picture.rebase(spheres=spheres, accelerations=accelerations)

        frame1 = frame2


main()
