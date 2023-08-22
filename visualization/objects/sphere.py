import random

from vpython import sphere, vector


class Sphere:
    def __init__(
            self,
            radius=0.5,
            color=(1.0, 0.0, 0.0),
            position=(0.0, 0.0, 0.0),
            rotation_angle_x=0.01,
            rotation_angle_y=0.0,
            picture=None
    ):
        if radius <= 0:
            raise ValueError("Radius must be a positive value")

        self.__radius = radius
        self.__position = position
        self.__rotation_angle_x = rotation_angle_x
        self.__rotation_angle_y = rotation_angle_y
        self.__color = color
        self.__picture = picture

        self.__shape = sphere(
            canvas=self.__picture.get_canvas(),
            pos=self.__position,
            radius=self.__radius,
            color=self.__color
        )

    def get_radius(self):
        return self.__radius

    def get_shape(self):
        return self.__shape

    def get_rotation_angle_x(self):
        return self.__rotation_angle_x

    def get_rotation_angle_y(self):
        return self.__rotation_angle_y

    def get_pos_x(self):
        return self.__shape.pos.x

    def get_pos_y(self):
        return self.__shape.pos.y

    def set_rotation_angle_x(self, a):
        self.__rotation_angle_x = a

    def set_rotation_angle_y(self, a):
        self.__rotation_angle_y = a

    def move(self, x, y):
        if not (-self.__picture.get_width() * self.__picture.get_canvas().range) <= (
                self.__shape.pos.x + x) * self.__picture.get_width() <= (
                       self.__picture.get_width() * self.__picture.get_canvas().range):
            x = 0

        if not (-self.__picture.get_height() * self.__picture.get_canvas().range) <= (
                self.__shape.pos.y + y) * self.__picture.get_height() <= (
                       self.__picture.get_height() * self.__picture.get_canvas().range):
            y = 0

        self.__shape.pos.x += x
        self.__shape.pos.y += y
