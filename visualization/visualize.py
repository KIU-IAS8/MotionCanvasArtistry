from vpython import rate, canvas
from mathematics.operations import coordinate_to_index_mapper, index_to_coordinate_mapper


class Picture:
    def __init__(
            self,
            height=400,
            width=400,
            factor=10,
            fps=30,
            scale=1.5,
            min_spheres=10000,
            max_spheres=20000,
            spawn_range=3,
            histogram=None,
            title="Title",
    ):
        self.__width = width
        self.__height = height
        self.__factor = factor
        self.__rate = fps
        self.__canvas = canvas(title=title, width=width, height=height)
        self.__canvas.range = scale
        self.__min_spheres = min_spheres
        self.__max_spheres = max_spheres
        self.__spawn_range=spawn_range
        self.__all_spheres = []
        self.__histogram = histogram

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

    def get_visible_spheres_count(self):
        return len([s for s in self.__all_spheres if s.get_shape().visible])

    def get_invisible_spheres(self):
        return [s for s in self.__all_spheres if not s.get_shape().visible]

    def get_random_invisible_sphere(self):
        for s in self.__all_spheres:
            if not s.get_shape().visible:
                return s
        return None

    def spawn(self, coordinates):
        s = self.get_random_invisible_sphere()
        s.make_visible(
            index_to_coordinate_mapper(coordinates[0], self.__factor, self.__width),
            index_to_coordinate_mapper(coordinates[1], self.__factor, self.__width)
        )

        return s

    def visualize(self):
        rate(self.__rate)

    def rebase(self, **objects):
        new_spheres = {}

        for c, s in objects["spheres"].items():
            if c in objects["displacements"].keys():
                s.move(objects["displacements"][c][0], objects["displacements"][c][1])
                k = f"{coordinate_to_index_mapper(s.get_pos_x(), self.__factor, self.__width)},{coordinate_to_index_mapper(s.get_pos_y(), self.__factor, self.__width)}"

                if ((s.get_shape_radius() >= (2 * s.get_radius()) and s.get_growing_status()) or
                        (s.get_shape_radius() <= (s.get_radius() / 3)) and not s.get_growing_status()):
                    s.inverse_growing()

                if s.get_growing_status():
                    if s.get_shape_radius() < s.get_radius():
                        s.grow_fast()
                    else:
                        s.grow()
                else:
                    s.reduce()

                if k not in new_spheres.keys():
                    new_spheres.update({k: s})

                else:
                    if s.get_shape_radius() >= (s.get_radius() / 10):
                        s.make_invisible()
                        if self.get_visible_spheres_count() <= self.__min_spheres:
                            c = self.__histogram.find_minimum_coordinates(new_spheres.keys())
                            ss = self.spawn(c)
                            new_spheres.update({f"{c[0]},{c[1]}": ss})

            else:
                if s.get_shape_radius() >= (s.get_radius() / 10):
                    s.make_invisible()
                    if self.get_visible_spheres_count() <= self.__min_spheres:
                        c = self.__histogram.find_minimum_coordinates(new_spheres.keys())
                        ss = self.spawn(c)
                        new_spheres.update({f"{c[0]},{c[1]}": ss})

        return new_spheres
