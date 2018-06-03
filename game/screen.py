

SPACING_X = 32
SPACING_Y = 16



class Screen:
    def __init__(self, camera, w, h):
        self.camera = camera
        self.width = w
        self.height = h
        self.pixel_size_x = 2 / w
        self.pixel_size_y = 2 / h

    def get_position(self, x, y, z, info):
        dx = SPACING_X / 2 * self.pixel_size_x * self.camera.zoom
        dy = SPACING_Y / 2 * self.pixel_size_y * self.camera.zoom
        dz = SPACING_Y * self.pixel_size_y * self.camera.zoom
        ox = info.offset_x * self.pixel_size_x * self.camera.zoom
        oy = info.offset_y * self.pixel_size_y * self.camera.zoom
        return (x * dx + y * dx - self.camera.x + ox, y * dy + x * -dy - self.camera.y + oy + z * dz)

    def get_tile_scale(self, info):
        return (info.width * self.pixel_size_x * self.camera.zoom,
                info.height * self.pixel_size_y * self.camera.zoom)
