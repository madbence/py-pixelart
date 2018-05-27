class Spring:
    def __init__(self, current, k=.1, d=.5):
        self.current = self.target = current
        self.k = k
        self.d = d
        self.v = 0

    def update(self):
        diff = self.target - self.current
        force = diff * self.k
        self.v += force - self.v * self.d
        self.current += self.v


