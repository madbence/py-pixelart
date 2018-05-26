TILE_WIDTH = 32
TILE_HEIGHT = 17
TILE_OFFSET_X = 0
TILE_OFFSET_Y = -1


class Screen:
    def __init__(self, w, h, s):
        self.width = w
        self.height = h
        self.scale = s
        self.pixel_size_x = 2 / w * s
        self.pixel_size_y = 2 / h * s

    def get_position(self, x, y):
        dx = (TILE_WIDTH + TILE_OFFSET_X) / 2 * self.pixel_size_x
        dy = (TILE_HEIGHT + TILE_OFFSET_Y) / 2 * self.pixel_size_y
        return (x * dx + y * dx, y * dy + x * -dy)

    def get_tile_scale(self):
        return (TILE_WIDTH * self.pixel_size_x, TILE_HEIGHT * self.pixel_size_y)
