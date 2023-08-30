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

    def calculate_proportion(self, spheres, count):
        result = []

        for k, v in sorted(self.__histogram.items(), key=lambda m: m[1]):
            if count <= 0:
                return result
            if k not in spheres:
                result.append(k)
                count -= 1

        return result
