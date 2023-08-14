import random
import time

from vpython import rate, vector, canvas


class Picture:
    def __init__(
            self,
            height=400,
            width=400,
            factor=10,
            fps=30,
            scale=1.5,
            title="Title",
    ):
        self.__width = width
        self.__height = height
        self.__factor = factor
        self.__rate = fps
        self.__canvas = canvas(title=title, width=width, height=height)
        self.__canvas.range = scale

    def get_rate(self):
        return self.__rate

    def set_rate(self, new_rate):
        self.__rate = new_rate

    def get_canvas(self):
        return self.__canvas

    def get_factor(self):
        return self.__factor

    def get_height(self):
        return self.__height

    def get_width(self):
        return self.__width

    def visualize(self, **objects):
        time.sleep(3)
        while True:
            rate(self.__rate)
            for sphere in objects["spheres"]:
                sphere.rebase(random.uniform(-0.0005, 0.0005), random.uniform(-0.0005, 0.0005))
