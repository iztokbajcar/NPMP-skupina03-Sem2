from component import Component
from enum import Enum


class CellFunction(Enum):
    INPUT = "INPUT"
    NORMAL = "NORMAL"
    OUTPUT = "OUTPUT"
    FIXED = "FIXED"


class Cell(Component):
    def __init__(
        self,
        x: float,
        y: float,
        function: CellFunction = CellFunction.NORMAL,
        clock: int = -1,
        label: str | None = None,
    ):
        super().__init__()
        self.x = x
        self.y = y
        self.function = function
        self.clock = clock
        self.label = label

    def __str__(self) -> str:
        return f"Cell '{self.label if self.label is not None else ''}' {{  {self.function.value}, ({self.x}, {self.y}), clock {self.clock}  }}"

    def get_id(self):
        return f"{self.x}_{self.y}"

    def get_name(self):
        if self.label is not None:
            return self.label
        else:
            return self.get_id()

    def get_color(self):
        if self.function == CellFunction.INPUT:
            return "blue"
        elif self.function == CellFunction.OUTPUT:
            return "yellow"
        elif self.function == CellFunction.FIXED:
            return "orange"
        else:
            if self.clock == 0:
                return "lime"
            elif self.clock == 1:
                return "magenta"
            elif self.clock == 2:
                return "cyan"
            else:
                return "white"

    def get_shape(self):
        return "dot"

    def determine_polarization(self, node, graph, visited, clk0, clk1, clk2, clk3):
        cell = node.value

        if cell.function == CellFunction.INPUT:
            # the polarization of an input cell is determined by the clock
            print("The cell is an input cell")
            if cell.clock == 0:
                cell.polarization = clk0
            elif cell.clock == 1:
                cell.polarization = clk1
            elif cell.clock == 2:
                cell.polarization = clk2
            else:
                cell.polarization = clk3
        else:
            neighbors = graph.component_neighbors(cell)
            polarized_neighbors = []

            for n in neighbors:
                if n.value.polarization is not None:
                    polarized_neighbors.append(n)

            # assume the value of the first polarized neighbor
            if len(polarized_neighbors) == 0:
                return None
            else:
                return polarized_neighbors[0].value.polarization
