from enum import Enum


class CellFunction(Enum):
    INPUT = "INPUT"
    NORMAL = "NORMAL"
    OUTPUT = "OUTPUT"


class Cell:
    def __init__(
        self,
        x: float,
        y: float,
        function: CellFunction = CellFunction.NORMAL,
        clock: int = -1,
    ):
        self.x = x
        self.y = y
        self.function = function
        self.clock = clock

    def __str__(self) -> str:
        return f"Cell {{  {self.function.value}, ({self.x}, {self.y}), clock {self.clock}  }}"
