import random

import glfw
from OpenGL.GL import *


def terminate():
    glfw.terminate()


class Picture:
    def __init__(self, height=400, width=400, factor=10, title="Title"):
        glfw.init()
        self.__window = glfw.create_window(width, height, title, None, None)

        glfw.make_context_current(self.__window)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

        self.__width = width
        self.__height = height
        self.__factor = factor

    def get_factor(self):
        return self.__factor

    def get_height(self):
        return self.__height

    def get_width(self):
        return self.__width

    def visualize(self, **objects):
        while not glfw.window_should_close(self.__window):
            glfw.poll_events()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            for sphere in objects["spheres"]:
                sphere.accelerate(a_x=0.00001, a_y=0.00001)
                sphere.rebase()
                sphere.draw()

            glfw.swap_buffers(self.__window)
