from OpenGL.GL import *
from OpenGL.GL import shaders


def create_shader(vertex_shader_src, fragment_shader_src):
    vertex_shader = shaders.compileShader(vertex_shader_src, GL_VERTEX_SHADER)
    fragment_shader = shaders.compileShader(fragment_shader_src, GL_FRAGMENT_SHADER)
    return shaders.compileProgram(vertex_shader, fragment_shader)
