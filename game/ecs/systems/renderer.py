from game.ecs import System, get_component

from game.ecs.components.transformation import Transformation
from game.ecs.components.sprite import Sprite


class Renderer(System):
    def __init__(self, screen):
        self.sprites = {}
        self.screen = screen

    def run(self, entities):
        for entity in entities:
            sprite = get_component(entity, Sprite)
            transform = get_component(entity, Transformation)
            self.sprites[sprite.name].render(self.screen, transform)
