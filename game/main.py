import glfw

from OpenGL.GL import *

from game.tile import BaseTileRenderer, Tile
from game.screen import Screen


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

    window = create_window(800, 600, fullscreen=False)
    screen = Screen(800, 600, 2)

    tile_renderer = BaseTileRenderer(screen)
    tiles = [Tile(x, y) for x in range(-5, 5) for y in range(-5, 5)]

    glfw.set_key_callback(window, key_callback)

    glClearColor(.5, .5, .5, 1)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)
        for tile in tiles:
            tile_renderer.draw(tile)
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()
