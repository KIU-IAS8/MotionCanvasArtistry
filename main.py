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
import sys


def initialize(
        device_id=0,
        factor=10,
        width=360,
        height=360,
        black_depth=-1,
        min_spheres=10000,
        max_spheres=20000,
        spawn_range=3,
        grow_speed=1,
        image_path="mock_data/images/img2.png"
):
    camera = VideoCaptureDevice(
        device_id=device_id,
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
        min_spheres=min_spheres,
        max_spheres=max_spheres,
        spawn_range=spawn_range,
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
                    grow_speed=grow_speed,
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


def run(
        device_id=1,
        factor=10,
        width=480,
        height=480,
        black_depth=-1,
        speed=5,
        spawn_range=2,
        grow_speed=2,
        image_path="mock_data/images/mock5.jpg"
):
    camera, picture, image, spheres, histogram = initialize(
        device_id=device_id,
        factor=factor,
        width=width,
        height=height,
        black_depth=black_depth,
        image_path=image_path,
        min_spheres=(width * height // factor // factor) - 1000,
        max_spheres=width * height // factor // factor,
        spawn_range=spawn_range,
        grow_speed=grow_speed
    )

    time.sleep(3)

    frame1 = convert_to_grayscale_cv2(camera.capture_frame())

    while True:
        rate(picture.get_rate())

        frame = camera.capture_frame()
        frame2 = convert_to_grayscale_cv2(frame)
        flow = cv2.calcOpticalFlowFarneback(frame1, frame2, None, 0.5, 3, 15, 3, 5, 1.1, 0)
        flow = cv2.resize(flow, (width, height), interpolation=cv2.INTER_CUBIC)
        force = optical_flow_interpolation(flow, 4)

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
        cv2.imshow("Live Camera", cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE))
        if cv2.waitKey(1) & 0xFF == ord("q"):
            raise SystemExit


if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            run(
                device_id=int(sys.argv[1]),
                factor=int(sys.argv[2]),
                width=int(sys.argv[3]),
                height=int(sys.argv[4]),
                black_depth=int(sys.argv[5]),
                speed=int(sys.argv[6]),
                spawn_range=int(sys.argv[7]),
                grow_speed=int(sys.argv[8]),
                image_path=f"mock_data/images/{sys.argv[9]}.jpg"
            )
        else:
            run()
    except Exception:
        run()
