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
        color = """+ color +  """
        FragColor = vec4(color, 1.0);
    }
    """

    return {
        "vertex": vertex_shader,
        "fragment": fragment_shader
    }
