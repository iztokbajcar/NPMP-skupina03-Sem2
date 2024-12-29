from gate import Gate, GateType


class Negator(Gate):
    def __init__(self):
        super().__init__(GateType.NEGATOR)

    def determine_polarization(self, node, graph, visited, clk0, clk1, clk2, clk3):
        neighbors = graph.component_neighbors(node.value)

        # assume the inverse value of the first found polarized neighbor
        for n in neighbors:
            if n.value.polarization is not None:
                self.polarization = 1 if n.value.polarization == 0 else 0
                return self.polarization
