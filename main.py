from tools.camera_integration import VideoCaptureDevice
from transformations.conversions import convert_to_grayscale_cv2
from visualization.objects.sphere import Sphere
from visualization.visualize import Picture
from mathematics.operations import rotate_matrix_right, index_to_coordinate_mapper
from mathematics.flow_interpolation import optical_flow_interpolation
from mathematics.histogram import Histogram
from vpython import vector, rate
import time
import cv2


def initialize(factor=10, width=360, height=360, black_depth=-1, necessary_spheres=10000, image_path="mock_data/images/img2.png"):
    camera = VideoCaptureDevice(
        width=width,
        height=height
    )

    histogram = Histogram(
        height=height,
        width=width,
        factor=factor
    )

    picture = Picture(
        factor=factor,
        height=height,
        width=width,
        necessary_spheres=necessary_spheres,
        fps=30,
        scale=1,
        histogram=histogram,
        title=image_path
    )

    image = rotate_matrix_right(cv2.imread(image_path))

    spheres = {}

    for x in range(0, len(image), factor):
        for y in range(0, len(image), factor):
            if image[x][y][0] > black_depth and image[x][y][1] > black_depth and image[x][y][2] > black_depth:
                s = Sphere(
                    picture=picture,
                    position=vector(
                        index_to_coordinate_mapper(x, factor, len(image)),
                        index_to_coordinate_mapper(y, factor, len(image)),
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
                picture.add_sphere(s)
                spheres.update({f"{x},{y}": s})

    return camera, picture, image, spheres, histogram


def run(factor=10, width=360, height=360, black_depth=-1, speed=5, necessary_spheres=10000, image_path="mock_data/images/mock4.jpg"):
    camera, picture, image, spheres, histogram = initialize(
        factor=factor,
        width=width,
        height=height,
        black_depth=black_depth,
        image_path=image_path,
        necessary_spheres=necessary_spheres
    )

    time.sleep(1)

    frame1 = convert_to_grayscale_cv2(camera.capture_frame())

    while True:
        rate(picture.get_rate())

        frame2 = convert_to_grayscale_cv2(camera.capture_frame())
        flow = cv2.calcOpticalFlowFarneback(frame1, frame2, None, 0.5, 3, 15, 3, 5, 1.1, 0)
        force = optical_flow_interpolation(flow)

        displacements = {}

        x = 0

        for i in range((force.shape[0] - height) // 2, (force.shape[0] + height) // 2, factor):
            y = 0
            for j in range((force.shape[1] - width) // 2, (force.shape[1] + width) // 2, factor):
                displacements.update({f"{x},{y}": (force[i][j][0] / (1000 / speed), force[i][j][1] / (1000 / speed))})
                y += factor
            x += factor

        spheres = picture.rebase(spheres=spheres, displacements=displacements)
        histogram.write_history(spheres.keys())

        frame1 = frame2
        cv2.imshow("test", cv2.rotate(frame1, cv2.ROTATE_90_COUNTERCLOCKWISE))
        if cv2.waitKey(1) & 0xFF == ord("q"):
            raise SystemExit


if __name__ == "__main__":
    run()
