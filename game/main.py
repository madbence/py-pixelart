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

    tile_renderer = BaseTileRenderer(screen, 'grid.png', TILE_MAP['floor'])
    wall_renderer_nw = BaseTileRenderer(screen, 'wall-nw.png', TILE_MAP['wall_nw'])
    wall_renderer_se = BaseTileRenderer(screen, 'wall-nw.png', TILE_MAP['wall_se'])
    wall_renderer_ne = BaseTileRenderer(screen, 'wall-ne.png', TILE_MAP['wall_ne'])
    wall_renderer_sw = BaseTileRenderer(screen, 'wall-ne.png', TILE_MAP['wall_sw'])
    tiles = [Tile(x, y, 0) for x in range(-5, 5) for y in range(-5, 5)]
    walls_nw = [Tile(x, -5, 0) for x in range(-5, 5)]
    walls_se = [Tile(x, 4, z) for x in range(-5, 5) for z in range(0, 2)]
    walls_ne = [Tile(4, y, 0) for y in range(-5, 5)]
    walls_sw = [Tile(-5, y, 0) for y in range(-5, 5)]
    ceiling = Tile(0, 0, 1)

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

        for tile in tiles:
            tile_renderer.draw(tile)
        for wall in walls_sw:
            wall_renderer_sw.draw(wall)
        for wall in walls_se:
            wall_renderer_se.draw(wall)
        for wall in walls_nw:
            wall_renderer_nw.draw(wall)
        for wall in walls_ne:
            wall_renderer_ne.draw(wall)
        tile_renderer.draw(ceiling)
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()
