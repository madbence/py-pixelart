import ctypes
import numpy as np

from OpenGL.GL import *
from PIL import Image

from game.shader import create_shader


class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class TileRenderer:
    def __init__(self, shader, vao, texture, screen):
        self._shader = shader
        self._vao = vao
        self._texture = texture
        self._screen = screen

    def draw(self, tile):
        glUseProgram(self._shader)
        glBindVertexArray(self._vao)
        glBindTexture(GL_TEXTURE_2D, self._texture)
        (tx, ty) = self._screen.get_position(tile.x, tile.y)
        (sx, sy) = self._screen.get_tile_scale()
        mx = np.array([[sx, 0, 0, 0],
                       [0, sy, 0, 0],
                       [0, 0, 1, 0],
                       [tx, ty, 0, 1]], 'f')
        glUniformMatrix4fv(0, 1, False, mx)
        glDrawArrays(GL_TRIANGLES, 0, 6)


class BaseTileRenderer(TileRenderer):
    def __init__(self, screen):
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
                color = vec4(Tex.xy, 0, 1);
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

        img = Image.open('grid.png').transpose(Image.FLIP_TOP_BOTTOM)
        img_data = np.fromstring(img.tobytes(), np.uint8)

        glBindTexture(GL_TEXTURE_2D, tex)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, 32, 17, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

        super(BaseTileRenderer, self).__init__(shader, vao, tex, screen)

