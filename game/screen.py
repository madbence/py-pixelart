import numpy as np


SPACING_X = 32
SPACING_Y = 16


class Screen:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.pixel_size_x = 2 / w
        self.pixel_size_y = 2 / h

    def transform(self, camera, zoom, x, y, z, info):
        dx = SPACING_X / 2 * self.pixel_size_x * zoom
        dy = SPACING_Y / 2 * self.pixel_size_y * zoom
        dz = SPACING_Y * self.pixel_size_y * zoom
        ox = info.offset_x * self.pixel_size_x * zoom
        oy = info.offset_y * self.pixel_size_y * zoom
        tx = x * dx + y * dx - camera.x + ox
        ty = y * dy + x * -dy - camera.y + oy + z * dz
        sx = info.width * self.pixel_size_x * zoom
        sy = info.height * self.pixel_size_y * zoom

        return np.array([[sx, 0, 0, 0],
                         [0, sy, 0, 0],
                         [0, 0, 1, 0],
                         [tx, ty, 0, 1]], 'f')
