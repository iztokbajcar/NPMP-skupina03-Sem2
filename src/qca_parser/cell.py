class Cell:
    def __init__(self, x, y, clock=-1):
        self.x = x
        self.y = y
        self.clock = clock

    def __str__(self):
        return f"Cell({self.x}, {self.y}, {self.clock})"
