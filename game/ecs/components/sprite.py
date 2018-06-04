from game.ecs import Component


class Sprite(Component):
    def __init__(self, name):
        self.name = name
