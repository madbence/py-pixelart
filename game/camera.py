from game.spring import Spring


class Camera:
    def __init__(self):
        self.zoom = 1
        self._x = Spring(0)
        self._y = Spring(0)

    def move(self, dx, dy):
        self._x.target += dx
        self._y.target += dy

    def update(self):
        self._x.update()
        self._y.update()

    @property
    def x(self):
        return self._x.current

    @property
    def y(self):
        return self._y.current
