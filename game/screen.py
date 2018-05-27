class TileInfo:
    def __init__(self, width, height, offset_x=0, offset_y=0):
        self.width = width
        self.height = height
        self.offset_x = offset_x
        self.offset_y = offset_y


def _describe(name, **kwargs):
    return (name, TileInfo(**kwargs))


SPACING_X = 32
SPACING_Y = 16

TILE_MAP = dict([
    _describe('floor', width=32, height=17),
    _describe('wall_nw', width=17, height=25, offset_x=-1),
])


class Screen:
    def __init__(self, camera, w, h):
        self.camera = camera
        self.width = w
        self.height = h
        self.pixel_size_x = 2 / w
        self.pixel_size_y = 2 / h

    def get_position(self, x, y, t):
        tile = TILE_MAP[t]
        dx = SPACING_X / 2 * self.pixel_size_x * self.camera.zoom
        dy = SPACING_Y / 2 * self.pixel_size_y * self.camera.zoom
        ox = tile.offset_x * self.pixel_size_x * self.camera.zoom
        oy = tile.offset_y * self.pixel_size_y * self.camera.zoom
        return (x * dx + y * dx - self.camera.x + ox, y * dy + x * -dy - self.camera.y + oy)

    def get_tile_scale(self, t):
        tile = TILE_MAP[t]
        return (tile.width * self.pixel_size_x * self.camera.zoom,
                tile.height * self.pixel_size_y * self.camera.zoom)
