from vpython import rate, canvas
from mathematics.operations import coordinate_to_index_mapper


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

    def visualize(self):
        rate(self.__rate)

    def rebase(self, **objects):
        new_spheres = {}

        for c, s in objects["spheres"].items():
            if c in objects["accelerations"].keys():
                s.move(objects["accelerations"][c][0], objects["accelerations"][c][1])
            k = f"{coordinate_to_index_mapper(s.get_pos_x(), self.__factor, self.__width)},{coordinate_to_index_mapper(s.get_pos_y(), self.__factor, self.__width)}"
            new_spheres.update({k: s})

        return new_spheres
