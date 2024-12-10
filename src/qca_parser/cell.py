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
        label: str | None = None,
    ):
        self.x = x
        self.y = y
        self.function = function
        self.clock = clock
        self.label = label

    def __str__(self) -> str:
        return f"Cell '{self.label if self.label is not None else ''}' {{  {self.function.value}, ({self.x}, {self.y}), clock {self.clock}  }}"

    def get_id(self):
        return f"{self.x}_{self.y}"

    def get_color(self):
        if self.function == CellFunction.INPUT:
            return "blue"
        elif self.function == CellFunction.OUTPUT:
            return "yellow"
        else:
            if self.clock == 0:
                return "green"
            elif self.clock == 1:
                return "magenta"
            elif self.clock == 2:
                return "cyan"
            else:
                return "white"
