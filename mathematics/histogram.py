class Histogram:
    def __init__(
            self,
            height=400,
            width=400,
            factor=10,
    ):
        self.__width = width
        self.__height = height
        self.__factor = factor
        self.__histogram = {}
        for x in range(0, height, factor):
            for y in range(0, width, factor):
                self.__histogram.update({f"{x},{y}": 1})

    def write_history(self, spheres):
        for x, y in spheres.items():
            self.__histogram.update({x:  self.__histogram[x]+y})

    def find_minimum_cord(self, spheres):
        minimum = ("0,0", self.__histogram['0,0'])
        for k, v in self.__histogram.items():
            if v < minimum[1] and k not in spheres:
                minimum = (k, v)

        coordinate = minimum[0].split(',')
        return int(coordinate[0]), int(coordinate[1])
