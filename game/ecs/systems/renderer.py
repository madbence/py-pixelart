from game.ecs import System, get_component

from game.ecs.components.transformation import Transformation
from game.ecs.components.sprite import Sprite
from game.ecs.components.camera_target import CameraTarget


class Renderer(System):
    def __init__(self, screen, camera):
        self.sprites = {}
        self.screen = screen
        self.camera = camera

    def run(self, entities):
        camera_position = get_component(self.camera, Transformation)
        zoom = get_component(self.camera, CameraTarget).zoom
        for entity in entities:
            sprite = get_component(entity, Sprite)
            transform = get_component(entity, Transformation)
            self.sprites[sprite.name].render(self.screen, camera_position, zoom, transform)
