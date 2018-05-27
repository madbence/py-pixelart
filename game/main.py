import glfw

from OpenGL.GL import *

from game.tile import BaseTileRenderer, Tile
from game.screen import Screen, TILE_MAP
from game.camera import Camera


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

        zoom_levels = [s/2 for s in range(1, 9)]

        if key == 256:
            glfw.set_window_should_close(window, True)
        if action == 1 or action == 2:
            if key == 61 and mods == 1:
                camera.zoom = zoom_levels[min(len(zoom_levels) - 1, zoom_levels.index(camera.zoom) + 1)]
            if key == 47 and mods == 0:
                camera.zoom = zoom_levels[max(0, zoom_levels.index(camera.zoom) - 1)]
            if key == 65 and mods == 0:
                camera.x -= .1
            if key == 68 and mods == 0:
                camera.x += .1
            if key == 83 and mods == 0:
                camera.y -= .1
            if key == 87 and mods == 0:
                camera.y += .1

    window = create_window(800, 600, fullscreen=False)
    camera = Camera()
    screen = Screen(camera, 800, 600, 2)

    tile_renderer = BaseTileRenderer(screen, 'grid.png', TILE_MAP['floor'])
    wall_renderer = BaseTileRenderer(screen, 'wall-nw.png', TILE_MAP['wall_nw'])
    tiles = [Tile(x, y) for x in range(-5, 5) for y in range(-5, 5)]
    walls = [Tile(x, 0, 'wall_nw') for x in range(0, 5)]

    glfw.set_key_callback(window, key_callback)

    glClearColor(.5, .5, .5, 1)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)
        for tile in tiles:
            tile_renderer.draw(tile)
        for wall in walls:
            wall_renderer.draw(wall)
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()
