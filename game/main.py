import glfw

from OpenGL.GL import *

from game.tile import Tile
from game.screen import Screen
from game.sprite import create_sprite_renderer
from game.camera import Camera

from game.ecs import Entity, Transform, Sprite, Render, add_component


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
                camera.zoom = min(9, max(1, camera.zoom + 1))
            if key == 47 and mods == 0:
                camera.zoom = min(9, max(1, camera.zoom - 1))
        if action == 1:
            if key == 65 and mods == 0:
                camera.move(-.02, 0)
            if key == 68 and mods == 0:
                camera.move(.02, 0)
            if key == 83 and mods == 0:
                camera.move(0, -.02)
            if key == 87 and mods == 0:
                camera.move(0, .02)
        if action == 0:
            if key == 65 and mods == 0:
                camera.move(.02, 0)
            if key == 68 and mods == 0:
                camera.move(-.02, 0)
            if key == 83 and mods == 0:
                camera.move(0, .02)
            if key == 87 and mods == 0:
                camera.move(0, -.02)

    window = create_window(800, 600, fullscreen=False)
    camera = Camera()
    screen = Screen(camera, 800, 600)

    floor_renderer = create_sprite_renderer('floor')

    renderer = Render(screen)
    renderer.sprites['floor'] = floor_renderer

    entities = []
    for x in range(-5, 5):
        for y in range(-5, 5):
            entity = Entity()
            add_component(entity, Transform(x, y, 0))
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
            camera.update()
            last += dt

        renderer.run(entities)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()
