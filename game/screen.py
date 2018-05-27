TILE_WIDTH = 32
TILE_HEIGHT = 17
TILE_OFFSET_X = 0
TILE_OFFSET_Y = -1


class Screen:
    def __init__(self, camera, w, h, s):
        self.camera = camera
        self.width = w
        self.height = h
        self.scale = s
        self.pixel_size_x = 2 / w * s
        self.pixel_size_y = 2 / h * s

    def get_position(self, x, y):
        dx = (TILE_WIDTH + TILE_OFFSET_X) / 2 * self.pixel_size_x * self.camera.zoom
        dy = (TILE_HEIGHT + TILE_OFFSET_Y) / 2 * self.pixel_size_y * self.camera.zoom
        return (x * dx + y * dx + self.camera.x, y * dy + x * -dy + self.camera.y)

    def get_tile_scale(self):
        return (TILE_WIDTH * self.pixel_size_x * self.camera.zoom,
                TILE_HEIGHT * self.pixel_size_y * self.camera.zoom)
