class TileInfo:
    def __init__(self, width, height, offset_x, offset_y, global_offset_x = 0, global_offset_y = 0):
        self.width = width
        self.height = height
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.global_offset_x = global_offset_x
        self.global_offset_y = global_offset_y


def _describe(name, **kwargs):
    return (name, TileInfo(**kwargs))


TILE_MAP = dict([
    _describe('floor', width=32, height=17, offset_x=0, offset_y=-1),
    _describe('wall_nw', width=17, height=25, offset_x=32 - 17, offset_y=-9, global_offset_x = -1),
])

class Screen:
    def __init__(self, camera, w, h, s):
        self.camera = camera
        self.width = w
        self.height = h
        self.scale = s
        self.pixel_size_x = 2 / w * s
        self.pixel_size_y = 2 / h * s

    def get_position(self, x, y, t):
        tile = TILE_MAP[t]
        dx = (tile.width + tile.offset_x) / 2 * self.pixel_size_x * self.camera.zoom
        dy = (tile.height + tile.offset_y) / 2 * self.pixel_size_y * self.camera.zoom
        ox = tile.global_offset_x * self.pixel_size_x * self.camera.zoom
        oy = tile.global_offset_y * self.pixel_size_y * self.camera.zoom
        return (x * dx + y * dx + self.camera.x + ox, y * dy + x * -dy + self.camera.y + oy)

    def get_tile_scale(self, t):
        tile = TILE_MAP[t]
        return (tile.width * self.pixel_size_x * self.camera.zoom,
                tile.height * self.pixel_size_y * self.camera.zoom)
