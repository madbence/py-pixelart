import ctypes
import numpy as np

from OpenGL.GL import *
from PIL import Image

from game.shader import create_shader


class SpriteInfo:
    def __init__(self, texture, width, height, offset_x=0, offset_y=0):
        self.texture = texture
        self.width = width
        self.height = height
        self.offset_x = offset_x
        self.offset_y = offset_y


SPRITE_MAP = {
    'floor': SpriteInfo(texture='grid.png', width=32, height=17),
    'wall_nw': SpriteInfo(texture='wall_nw.png', width=17, height=25, offset_x=-1),
    'wall_se': SpriteInfo(texture='wall_nw.png', width=17, height=25, offset_x=15, offset_y=8),
    'wall_ne': SpriteInfo(texture='wall_ne.png', width=17, height=25, offset_x=15),
    'wall_sw': SpriteInfo(texture='wall_ne.png', width=17, height=25, offset_x=-1, offset_y=8),
}


class SpriteRenderer:
    def __init__(self, shader, vao, texture, sprite_info):
        self._shader = shader
        self._vao = vao
        self._texture = texture
        self._sprite_info = sprite_info

    def render(self, screen, camera, zoom, tile):
        glUseProgram(self._shader)
        glBindVertexArray(self._vao)
        glBindTexture(GL_TEXTURE_2D, self._texture)
        mx = screen.transform(camera, zoom, tile.x, tile.y, tile.z, self._sprite_info)
        glUniformMatrix4fv(0, 1, False, mx)
        glDrawArrays(GL_TRIANGLES, 0, 6)


def create_sprite_renderer(sprite_name):
    sprite_info = SPRITE_MAP[sprite_name]
    shader = create_shader(vertex_shader_src='''
        #version 440 core

        layout(location = 0) in vec2 position;
        layout(location = 1) in vec2 tex;

        layout(location = 0) uniform mat4 model;

        out vec2 Tex;

        void main() {
            gl_Position = model * vec4(position, 0, 1);
            Tex = tex;
        }
    ''', fragment_shader_src='''
        #version 440 core

        in vec2 Tex;

        layout(location = 0) out vec4 color;

        uniform sampler2D tex;

        void main() {
            color = texture2D(tex, Tex);
        }
    ''')
    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)
    tex = glGenTextures(1)

    verts = np.array([[0, 0, 0, 0],
                      [0, 1, 0, 1],
                      [1, 1, 1, 1],
                      [1, 1, 1, 1],
                      [1, 0, 1, 0],
                      [0, 0, 0, 0]], 'f')

    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, 4 * 4 * 6, verts, GL_STATIC_DRAW)

    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 2, GL_FLOAT, False, 16, ctypes.c_void_p(0))
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, False, 16, ctypes.c_void_p(8))

    img = Image.open(sprite_info.texture).transpose(Image.FLIP_TOP_BOTTOM)
    img_data = np.fromstring(img.tobytes(), np.uint8)

    glBindTexture(GL_TEXTURE_2D, tex)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

    return SpriteRenderer(shader, vao, tex, sprite_info)
