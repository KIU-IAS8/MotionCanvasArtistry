from vpython import rate, vector


def visualize2(**objects):
    while True:
        rate(30)  # Limit the frame rate for smoother animation
        for sphere in objects["spheres"]:
            sphere.rotate(angle=0.01, axis=vector(0, 1, 0))