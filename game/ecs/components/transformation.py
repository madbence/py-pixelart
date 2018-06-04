from game.ecs import Component


class Transformation(Component):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
