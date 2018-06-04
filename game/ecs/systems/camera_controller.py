from game.ecs import System, get_component
from game.ecs.components.camera_target import CameraTarget
from game.ecs.components.transformation import Transformation


def update_spring(spring, current, dt):
    diff = spring.target - current
    force = diff * spring.k
    spring.v += force - spring.v * spring.d * dt
    return current + spring.v * dt


class CameraController(System):
    def run(self, camera_entity, dt):
        camera_target = get_component(camera_entity, CameraTarget)
        camera_position = get_component(camera_entity, Transformation)
        camera_position.x = update_spring(camera_target.x, camera_position.x, dt)
        camera_position.y = update_spring(camera_target.y, camera_position.y, dt)
        camera_target.x.target -= (camera_target.dx[0] - camera_target.dx[1]) / camera_target.zoom
        camera_target.y.target -= (camera_target.dy[0] - camera_target.dy[1]) / camera_target.zoom
