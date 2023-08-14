import OpenGL.GL as gl
from OpenGL.GL import shaders


def generate_shaders(color1=(1.0, 0.0, 0.0), color2=(0.0, 0.0, 1.0)):
    color = (f"mix(vec3({color1[0]}, {color1[1]}, {color1[2]}), "
             f"vec3({color2[0]}, {color2[1]}, {color2[2]}), "
             f"frag_position.y);  "
             f"// Gradient along the Y-axis")

    vertex_shader = """
    #version 330 core
    layout (location = 0) in vec3 a_position;
    out vec3 frag_position;

    uniform mat4 model;
    uniform mat4 view;
    uniform mat4 projection;

    void main()
    {
        gl_Position = projection * view * model * vec4(a_position, 1.0);
        frag_position = a_position;
    }
    """

    fragment_shader = """
    #version 330 core
    in vec3 frag_position;
    out vec4 FragColor;

    void main()
    {
        vec3 color = vec3(0.0);
        color = """ + color + """
        FragColor = vec4(color, 1.0);
    }
    """

    return {
        "vertex": vertex_shader,
        "fragment": fragment_shader
    }


def compile_shader(source, shader_type):
    shader = shaders.compileShader(source, shader_type)
    return shader


def unuse():
    gl.glUseProgram(0)


class ShaderProgram:
    def __init__(self):
        self.__shader_program = None

    def link_shaders(self, vertex_shader, fragment_shader):
        self.__shader_program = gl.glCreateProgram()
        gl.glAttachShader(self.__shader_program, vertex_shader)
        gl.glAttachShader(self.__shader_program, fragment_shader)
        gl.glLinkProgram(self.__shader_program)

        if not gl.glGetProgramiv(self.__shader_program, gl.GL_LINK_STATUS):
            info_log = gl.glGetProgramInfoLog(self.__shader_program)
            raise RuntimeError(f"Shader program linking failed: {info_log}")

    def use(self):
        gl.glUseProgram(self.__shader_program)

    def __del__(self):
        if self.__shader_program is not None:
            gl.glDeleteProgram(self.__shader_program)
