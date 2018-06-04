from game.ecs import Component


class CameraTarget(Component):
    def __init__(self, zoom, x, y, k, d):
        self.zoom = zoom
        self.x = Spring(x, k, d)
        self.y = Spring(y, k, d)
        self.dx = [0, 0]
        self.dy = [0, 0]


class Spring:
    def __init__(self, target, k, d):
        self.target = target
        self.v = 0
        self.k = k
        self.d = d
