from gate import Gate, GateType


class MajorityGate(Gate):
    def __init__(self, gate_id):
        super().__init__(GateType.MAJORITY)
        self.id = gate_id

    def get_id(self):
        return self.id

    def get_name(self):
        return f"MAJORITY ({self.id})"

    def determine_polarization(self, node, graph, visited, clk0, clk1, clk2, clk3):
        neighbors = graph.component_neighbors(node.value)

        # get all polarized_neighbors
        polarized_neighbors = []
        for n in neighbors:
            if n.value.polarization is not None:
                polarized_neighbors.append(n)

        # get the most common value of all
        # polarized neighbors
        if len(polarized_neighbors) == 0:
            return None

        polarized_values = [n.value.polarization for n in polarized_neighbors]
        most_common = max(polarized_values, key=polarized_values.count)
        print("  - values of polarized neighbors:", polarized_values)
        print("  - most common value:", most_common)

        self.polarization = most_common
        return self.polarization
