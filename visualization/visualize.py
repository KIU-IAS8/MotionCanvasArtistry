import glfw
from OpenGL.GL import *


def terminate():
    glfw.terminate()


class Picture:
    def __init__(self, height=1000, width=1000, title="Title"):
        glfw.init()
        self.__window = glfw.create_window(width, height, title, None, None)
        glfw.make_context_current(self.__window)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

        glEnable(GL_DEPTH_TEST)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def visualize(self, **objects):
        while not glfw.window_should_close(self.__window):
            glfw.poll_events()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            for sphere in objects["spheres"]:
                sphere.draw()
                sphere.update(0.001)

            glfw.swap_buffers(self.__window)
