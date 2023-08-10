import math
import numpy as np
from visualization.shaders import generate_shaders
from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.GL import *


class Sphere:
    def __init__(self, radius=0.5, start_color=(1.0, 0.0, 0.0), end_color=(0.0, 0.0, 1.0), slices=30,
                 stacks=30,
                 position=(0.0, 0.0, 0.0), speed=(0.8, 0.8, 0.0), rotation_angle=45, rotation_speed=1):
        if radius <= 0:
            raise ValueError("Radius must be a positive value")

        self.__radius = radius
        self.__position = np.array(position)
        self.__speed = speed
        self.__rotation_angle = rotation_angle
        self.__rotation_speed = rotation_speed

        shaders = generate_shaders(start_color, end_color)

        self.__fragment_shader = shaders["fragment"]
        self.__vertex_shader = shaders["vertex"]

        self.__slices = slices
        self.__stacks = stacks

        self.__vertices = self.create_sphere_vertices()
        self.__vertices = np.array(self.__vertices).reshape(-1, 3)

        self.__shader_program = compileProgram(
            compileShader(self.__vertex_shader, GL_VERTEX_SHADER),
            compileShader(self.__fragment_shader, GL_FRAGMENT_SHADER)
        )

        self.__vao = glGenVertexArrays(1)
        glBindVertexArray(self.__vao)

        self.__vbo = glGenBuffers(1)

        self.create_vao_vbo()

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * ctypes.sizeof(GLfloat), ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

        self.__model = np.identity(4, dtype=np.float32)
        self.__view = np.identity(4, dtype=np.float32)
        self.__projection = np.identity(4, dtype=np.float32)

    def get_radius(self):
        return self.__radius

    def get_speed(self):
        return self.__speed

    def get_rotation_angle(self):
        return self.__rotation_angle

    def get_rotation_speed(self):
        return self.__rotation_speed

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

    def set_speed(self, new_speed):
        self.__speed = new_speed

    def set_rotation_angle(self, new_rotation_angle):
        self.__rotation_angle = new_rotation_angle

    def set_rotation_speed(self, new_rotation_speed):
        self.__rotation_speed = new_rotation_speed

    def accelerate(self, a_x=0.0, a_y=0.0, a_z=0.0):
        self.__speed = (self.__speed[0] + a_x, self.__speed[1] + a_y, self.__speed[2] + a_z)

    def change_colors(self, new_start_color, new_end_color):
        self.__fragment_shader = generate_shaders(new_start_color, new_end_color)["fragment"]

    def create_sphere_vertices(self):
        vertices = []

        for lat in range(self.__slices + 1):
            theta = lat * np.pi / self.__slices
            sin_theta = np.sin(theta)
            cos_theta = np.cos(theta)

            for lon in range(self.__stacks + 1):
                phi = lon * 2 * np.pi / self.__stacks
                sin_phi = np.sin(phi)
                cos_phi = np.cos(phi)

                v_x = self.__radius * sin_theta * cos_phi + self.__position[0]
                v_y = self.__radius * sin_theta * sin_phi + self.__position[1]
                v_z = self.__radius * cos_theta + self.__position[2]

                vertices.extend([v_x, v_y, v_z])

        return np.array(vertices, dtype=np.float32)

    def create_vao_vbo(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.__vbo)
        glBufferData(GL_ARRAY_BUFFER, self.__vertices.nbytes, self.__vertices, GL_STATIC_DRAW)

    # def create_vao_vbo(self):
    #     self.__vao = glGenVertexArrays(1)
    #     glBindVertexArray(self.__vao)
    #
    #     self.__vbo = glGenBuffers(1)
    #     glBindBuffer(GL_ARRAY_BUFFER, self.__vbo)
    #     glBufferData(GL_ARRAY_BUFFER, self.__vertices.nbytes, self.__vertices, GL_STATIC_DRAW)
    #     glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * ctypes.sizeof(GLfloat), ctypes.c_void_p(0))
    #     glEnableVertexAttribArray(0)
    #
    #     glBindBuffer(GL_ARRAY_BUFFER, 0)
    #     glBindVertexArray(0)

    def rotate(self, rotation_axis):
        self.__vertices = np.array(self.__vertices).reshape(-1, 3)

        angle_radians = np.radians(self.__rotation_angle)

        if rotation_axis == 'x':
            rotation_matrix = np.array([
                [1, 0, 0],
                [0, np.cos(angle_radians), -np.sin(angle_radians)],
                [0, np.sin(angle_radians), np.cos(angle_radians)]
            ])
        elif rotation_axis == 'y':
            rotation_matrix = np.array([
                [np.cos(angle_radians), 0, np.sin(angle_radians)],
                [0, 1, 0],
                [-np.sin(angle_radians), 0, np.cos(angle_radians)]
            ])
        else:
            rotation_matrix = np.array([
                [np.cos(angle_radians), -np.sin(angle_radians), 0],
                [np.sin(angle_radians), np.cos(angle_radians), 0],
                [0, 0, 1]
            ])

        self.__vertices = np.dot(self.__vertices, rotation_matrix.T)

    def rotate_model(self):
        rotation_matrix = np.array([
            [math.cos(self.__rotation_angle), 0, -math.sin(self.__rotation_angle), 0],
            [0, 1, 0, 0],
            [math.sin(self.__rotation_angle), 0, math.cos(self.__rotation_angle), 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)
        self.__model = np.dot(self.__model, rotation_matrix)

    def move(self):
        for i in range(self.__vertices.shape[0]):
            if 0 <= self.__vertices[i][0] + self.__speed[0] <= 1:
                self.__vertices[i][0] += self.__speed[0]
            if 0 < self.__vertices[i][1] + self.__speed[1] <= 1:
                self.__vertices[i][1] += self.__speed[1]
            # if 0 <= self.__vertices[i][2] + self.__speed[2] <= 1:
            #     self.__vertices[i][2] += self.__speed[2]

    def draw(self):
        self.create_vao_vbo()
        glUseProgram(self.__shader_program)
        glBindVertexArray(self.__vao)
        glUniformMatrix4fv(glGetUniformLocation(self.__shader_program, "view"), 1, GL_FALSE, self.__view)
        glUniformMatrix4fv(glGetUniformLocation(self.__shader_program, "projection"), 1, GL_FALSE, self.__projection)
        glUniformMatrix4fv(glGetUniformLocation(self.__shader_program, "model"), 1, GL_FALSE, self.__model)
        glDrawArrays(GL_POLYGON, 0, self.__vertices.size // 3)
        glBindVertexArray(0)

    def rebase(self, rotation_axis='z'):
        self.move()
        # self.rotate_model()
        # self.rotate(rotation_axis)
