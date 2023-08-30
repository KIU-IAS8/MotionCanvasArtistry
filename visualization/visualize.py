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
        self.__all_spheres = []

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

    def get_all_spheres(self):
        return self.__all_spheres

    def add_sphere(self, sphere):
        self.__all_spheres.append(sphere)

    def get_visible_spheres(self):
        return [s for s in self.__all_spheres if s.get_shape().visible]

    def get_invisible_spheres(self):
        return [s for s in self.__all_spheres if not s.get_shape().visible]

    def visualize(self):
        rate(self.__rate)

    def rebase(self, **objects):
        new_spheres = {}

        for c, s in objects["spheres"].items():
            if c in objects["displacements"].keys():
                s.move(objects["displacements"][c][0], objects["displacements"][c][1])
                k = f"{coordinate_to_index_mapper(s.get_pos_x(), self.__factor, self.__width)},{coordinate_to_index_mapper(s.get_pos_y(), self.__factor, self.__width)}"

                if k not in new_spheres.keys():
                    new_spheres.update({k: s})
                else:
                    s.make_invisible()

            else:
                s.make_invisible()

        return new_spheres
