import glfw

from OpenGL.GL import *

from game.tile import Tile
from game.screen import Screen
from game.sprite import create_sprite_renderer

from game.ecs import Entity
from game.ecs.components.transformation import Transformation
from game.ecs.components.sprite import Sprite
from game.ecs.components.camera_target import CameraTarget
from game.ecs.systems.renderer import Renderer
from game.ecs.systems.camera_controller import CameraController
from game.ecs import add_component


def create_window(width, height, fullscreen):
    if not glfw.init():
        return None

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 4)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
    glfw.window_hint(glfw.RESIZABLE, False)

    if fullscreen:
        window = glfw.create_window(width, height, 'Hello World', glfw.get_primary_monitor(), None)
    else:
        window = glfw.create_window(width, height, 'Hello World', None, None)

    if not window:
        glfw.terminate()
        return None

    glfw.make_context_current(window)

    return window


def main():
    def key_callback(window, key, scancode, action, mods):
        print('key_callback', key, scancode, action, mods)

        if key == 256:
            glfw.set_window_should_close(window, True)
        if action == 1 or action == 2:
            if key == 61 and mods == 1:
                camera_target.zoom = min(9, max(1, camera_target.zoom + 1))
            if key == 47 and mods == 0:
                camera_target.zoom = min(9, max(1, camera_target.zoom - 1))
        if action == 1:
            if key == 65 and mods == 0:
                camera_target.dx[0] = .05
            if key == 68 and mods == 0:
                camera_target.dx[1] = .05
            if key == 83 and mods == 0:
                camera_target.dy[0] = .05
            if key == 87 and mods == 0:
                camera_target.dy[1] = .05
        if action == 0:
            if key == 65 and mods == 0:
                camera_target.dx[0] = 0
            if key == 68 and mods == 0:
                camera_target.dx[1] = 0
            if key == 83 and mods == 0:
                camera_target.dy[0] = 0
            if key == 87 and mods == 0:
                camera_target.dy[1] = 0

    camera = Entity()
    camera_target = CameraTarget(2, 0, 0, 5, 30)
    add_component(camera, camera_target)
    add_component(camera, Transformation(0, 0, 0))
    screen = Screen(800, 600)

    window = create_window(screen.width, screen.height, fullscreen=False)

    renderer = Renderer(screen, camera)
    renderer.sprites['floor'] = create_sprite_renderer('floor')

    camera_controller = CameraController()

    entities = []
    for x in range(-5, 5):
        for y in range(-5, 5):
            entity = Entity()
            add_component(entity, Transformation(x, y, 0))
            add_component(entity, Sprite('floor'))
            entities.append(entity)

    glfw.set_key_callback(window, key_callback)

    glClearColor(.5, .5, .5, 1)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    last = 0
    dt = .02
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)

        time = glfw.get_time()
        while last < time:
            last += dt
            camera_controller.run(camera, dt)

        renderer.run(entities)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()
