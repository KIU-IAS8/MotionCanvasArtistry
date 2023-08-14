import random

from vpython import sphere, vector


class Sphere:
    def __init__(
            self,
            radius=0.5,
            color=(1.0, 0.0, 0.0),
            position=(0.0, 0.0, 0.0),
            speed=(0.8, 0.8, 0.0),
            rotation_angle_x=0.01,
            rotation_angle_y=0.0,
            picture=None
    ):
        if radius <= 0:
            raise ValueError("Radius must be a positive value")

        self.__radius = radius
        self.__position = position
        self.__speed = speed
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

    def get_speed(self):
        return self.__speed

    def get_rotation_angle_x(self):
        return self.__rotation_angle_x

    def get_rotation_angle_y(self):
        return self.__rotation_angle_y

    def set_rotation_angle_x(self, a):
        self.__rotation_angle_x = a

    def set_rotation_angle_y(self, a):
        self.__rotation_angle_y = a

    def set_speed(self, new_speed):
        self.__speed = new_speed

    def accelerate(self, a_x=0.0, a_y=0.0, a_z=0.0):
        self.__speed = (self.__speed[0] + a_x, self.__speed[1] + a_y, self.__speed[2] + a_z)

    def move(self):
        speed_x = self.__speed[0]
        speed_y = self.__speed[1]
        if not (-self.__picture.get_width() * self.__picture.get_canvas().range) <= (
                self.__shape.pos.x + self.__speed[0]) * self.__picture.get_width() <= (
                       self.__picture.get_width() * self.__picture.get_canvas().range):
            speed_x = -self.__speed[0]

        if not (-self.__picture.get_height() * self.__picture.get_canvas().range) <= (
                self.__shape.pos.y + self.__speed[1]) * self.__picture.get_height() <= (
                       self.__picture.get_height() * self.__picture.get_canvas().range):
            speed_y = -self.__speed[1]

        self.__speed = (speed_x, speed_y, 0.0)

        self.__shape.pos.x += self.__speed[0]
        self.__shape.pos.y += self.__speed[1]

    def rebase(self, a_x, a_y):
        # self.__shape.rotate(angle=self.__rotation_angle_y, axis=vector(0, 1, 0))
        # self.__shape.rotate(angle=self.__rotation_angle_x, axis=vector(1, 0, 0))

        self.move()
        self.accelerate(a_x=a_x, a_y=a_y)

        # self.__shape = sphere(
        #     canvas=self.__canvas,
        #     pos=vector(self.__position),
        #     radius=self.__radius,
        #     color=vector(self.__color)
        # )
