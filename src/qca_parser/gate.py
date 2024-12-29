from component import Component
from enum import Enum


class GateType(Enum):
    NEGATOR = "NEGATOR"
    MAJORITY = "MAJORITY"


class Gate(Component):
    def __init__(self, type: GateType):
        super().__init__()
        self.type = type
        self.label = type.value

    def get_id(self):
        return f"{self.type.value}"

    def get_name(self):
        return f"{self.type.value}"

    def get_color(self):
        return "red"

    def get_shape(self):
        return "square"

    def determine_polarization(self, node, graph, visited, clk0, clk1, clk2, clk3):
        raise NotImplementedError
