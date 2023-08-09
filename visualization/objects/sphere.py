import math
import numpy as np
from visualization.shaders import generate_shaders
from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.GL import *


class Sphere:
    def __init__(self, radius=0.5, start_color=(1.0, 0.0, 0.0), end_color=(0.0, 0.0, 1.0), slices=30, stacks=900,
                 position=(0.0, 0.0, 0.0), speed=0.8, rotation_angle=1, projection=0.8,
                 window_width=1000, window_height=1000):
        if radius <= 0:
            raise ValueError("Radius must be a positive value")

        self.__radius = radius
        self.__position = np.array(position)
        self.__speed = speed
        self.__rotation_angle = rotation_angle

        shaders = generate_shaders(start_color, end_color)

        self.__fragment_shader = shaders["fragment"]
        self.__vertex_shader = shaders["vertex"]
        self.__slices = slices
        self.__stacks = stacks

        vertices = []
        for stack in range(self.__stacks + 1):
            phi = math.pi / self.__stacks * stack
            for slc in range(self.__slices + 1):
                theta = 2 * math.pi / self.__slices * slc
                x = radius * math.sin(phi) * math.cos(theta)
                y = radius * math.sin(phi) * math.sin(theta)
                z = radius * math.cos(phi)
                vertices.extend([x, y, z])

        self.__vertices = np.array(vertices, dtype=np.float32)
        self.__shader_program = compileProgram(compileShader(self.__vertex_shader, GL_VERTEX_SHADER),
                                               compileShader(self.__fragment_shader, GL_FRAGMENT_SHADER))
        self.__vao = None
        self.__vbo = None
        self.create_vao_vbo()

        aspect_ratio = window_width / window_height

        self.__model = np.identity(4, dtype=np.float32)
        self.__view = np.identity(4, dtype=np.float32)
        self.__projection = np.array([
            [projection / aspect_ratio, 0, 0, 0],
            [0, projection, 0, 0],
            [0, 0, -1.0, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)

    def get_radius(self):
        return self.__radius

    def get_speed(self):
        return self.__speed

    def get_rotation_angle(self):
        return self.__rotation_angle

    def get_view(self):
        return self.__view

    def get_projection(self):
        return self.__projection

    def get_vertices(self):
        return self.__vertices

    def get_vertex_shader(self):
        return self.__vertex_shader

    def get_fragment_shader(self):
        return self.__fragment_shader

    def get_shader_program(self):
        return self.__shader_program

    def get_vao(self):
        return self.__vao

    def get_vbo(self):
        return self.__vbo

    def change_colors(self, new_start_color, new_end_color):
        self.__fragment_shader = generate_shaders(new_start_color, new_end_color)["fragment"]

    def create_vao_vbo(self):
        self.__vao = glGenVertexArrays(1)
        glBindVertexArray(self.__vao)

        self.__vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.__vbo)
        glBufferData(GL_ARRAY_BUFFER, self.__vertices.nbytes, self.__vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * ctypes.sizeof(GLfloat), ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def translation_matrix(self):
        return np.array([
            [1, 0, 0, self.__position[0]],
            [0, 1, 0, self.__position[1]],
            [0, 0, 1, self.__position[2]],
            [0, 0, 0, 1]
        ], dtype=np.float32)

    def rotation_matrix(self):
        return np.array([
            [math.cos(self.__rotation_angle), 0, -math.sin(self.__rotation_angle), 0],
            [0, 1, 0, 0],
            [math.sin(self.__rotation_angle), 0, math.cos(self.__rotation_angle), 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)

    def movement_matrix(self):
        return np.array([
            [1, 0, 0, self.__speed * math.sin(self.__rotation_angle)],
            [0, 1, 0, 0],
            [0, 0, 1, self.__speed * math.cos(self.__rotation_angle)],
            [0, 0, 0, 1]
        ], dtype=np.float32)

    def scale_matrix(self):
        scale_matrix = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)

        np.fill_diagonal(scale_matrix, self.__radius)
        return scale_matrix

    def draw(self):
        glUseProgram(self.__shader_program)
        glBindVertexArray(self.__vao)
        glUniformMatrix4fv(glGetUniformLocation(self.__shader_program, "view"), 1, GL_FALSE, self.__view)
        glUniformMatrix4fv(glGetUniformLocation(self.__shader_program, "projection"), 1, GL_FALSE, self.__projection)
        glUniformMatrix4fv(glGetUniformLocation(self.__shader_program, "model"), 1, GL_FALSE, self.__model)
        glDrawArrays(GL_TRIANGLES, 0, self.__vertices.size // 3)
        glBindVertexArray(0)

    def update(self, plus_rotation_angle):
        self.__rotation_angle += plus_rotation_angle

        self.__model = np.identity(4, dtype=np.float32)
        self.__model = np.dot(self.__model, self.translation_matrix())
        self.__model = np.dot(self.__model, self.rotation_matrix())
        self.__model = np.dot(self.__model, self.movement_matrix())
        self.__model = np.dot(self.__model, self.scale_matrix())
