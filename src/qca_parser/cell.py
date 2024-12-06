class Cell:
    def __init__(self, x, y, diameter, spin, potential, clock=0):
        self.x = x
        self.y = y
        self.diameter = diameter
        self.spin = spin
        self.potential = potential
        self.clock = clock
