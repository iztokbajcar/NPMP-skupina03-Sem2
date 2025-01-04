from cell import Cell, CellFunction
from gate import Gate, GateType
from graph import Graph, GraphNode
from math import pi, sin
from negator import Negator
from matplotlib import pyplot as plt
import numpy as np


class Simulator:
    def __init__(self, graph: list[Cell]):
        self.graph = graph

    def get_clk0_value(self, t: float):
        """Returns the value of clk0 at time t."""
        return sin(t)

    def get_clk1_value(self, t: float):
        """Returns the value of clk1 at time t."""
        return sin(t + 3 * (pi / 2))

    def get_clk2_value(self, t: float):
        """Returns the value of clk2 at time t."""
        return sin(t + pi)

    def get_clk3_value(self, t: float):
        """Returns the value of clk3 at time t."""
        return sin(t + pi / 2)

    def determine_gate_polarization(
        self,
        node: GraphNode,
        graph: Graph,
        visited: list[GraphNode],
        clk0: float,
        clk1: float,
        clk2: float,
        clk3: float,
    ):
        component = node.value
        component.determine_polarization(node, graph, visited, clk0, clk1, clk2, clk3)

    def determine_node_polarization(
        self,
        node: GraphNode,
        graph: Graph,
        visited: list[GraphNode],
        clk0: float,
        clk1: float,
        clk2: float,
        clk3: float,
    ):
        """Returns the value of the cell based on the clock values and other cells."""
        if node.value.polarization is not None:
            return node.value.polarization

        # if the node is an input cell, return its polarization
        if isinstance(node.value, Cell) and node.value.function == CellFunction.INPUT:
            print(f"Component {node.value.get_name()} is an input cell")
            return node.value.polarization

        visited.append(node)

        # determine polarizations of unpolarized neighbors
        neighbors = graph.component_neighbors(node.value)
        polarized_neighbors = []

        for n in neighbors:
            if n.value.polarization is not None:
                polarized_neighbors.append(n)

        for n in neighbors:
            if n not in polarized_neighbors and n not in visited:
                self.determine_node_polarization(
                    n, graph, visited, clk0, clk1, clk2, clk3
                )

        # determine the polarization of the current node
        print(f"Processing cell '{node.value.get_name()}'")

        component = node.value

        polarization = component.determine_polarization(
            node, graph, visited, clk0, clk1, clk2, clk3
        )

        print(f"Determining polarization of {node.value.get_name()} as {polarization}")
        node.value.polarization = polarization
        return polarization

    def reset_cell_polarizations(self):
        for n in self.graph.nodes:
            if not (
                isinstance(n.value, Cell) and n.value.function == CellFunction.FIXED
            ):
                n.value.polarization = None

    def simulate(self, num_cycles: int, step: float):
        # extract input nodes
        inputs = []
        for n in self.graph.nodes:
            if isinstance(n.value, Cell) and n.value.function == CellFunction.INPUT:
                inputs.append(n)

        # extract output nodes
        outputs = []
        for n in self.graph.nodes:
            if isinstance(n.value, Cell) and n.value.function == CellFunction.OUTPUT:
                outputs.append(n)

        num_combinations = 2 ** len(inputs)
        smallest_input_duration = num_cycles / num_combinations
        print(
            f"Simulating {num_combinations} input combinations with step {step} for {num_cycles} clock cycles."
        )

        # initialize the list of input values
        input_values = []
        for i in range(0, len(inputs)):
            input_values.append([])

        # initialize the list of output values
        output_values = []
        for i in range(0, len(outputs)):
            output_values.append([])

        # initialize lists of values for clock signals
        clk_values = []
        for i in range(4):
            clk_values.append([])

        # initialize the dictionary of cell values
        cell_values = {}
        for n in self.graph.nodes:
            cell_values[n.value.get_id()] = []

        truth_table_values = []

        for comb in range(0, num_combinations):
            # simulate for smallest_input_duration steps

            for t in np.arange(
                comb * smallest_input_duration,
                (comb + 1) * smallest_input_duration,
                step,
            ):
                self.reset_cell_polarizations()
                input_vector = []

                # set input values
                for i, n in enumerate(inputs):
                    polarization = (comb >> (len(inputs) - 1 - i)) & 1
                    n.value.polarization = polarization
                    # print(
                    #     f"Cell {n.value.get_id()} (label {n.value.label}) set to {n.value.polarization}"
                    # )

                    input_vector.append(polarization)
                    input_values[i].append(polarization)

                print(f"============== Input vector: {input_vector}")

                clk0 = self.get_clk0_value(t * num_cycles)
                clk1 = self.get_clk1_value(t * num_cycles)
                clk2 = self.get_clk2_value(t * num_cycles)
                clk3 = self.get_clk3_value(t * num_cycles)

                # determine polarizations of cells by starting at
                # the output cells and recursively checking towards
                # the input cells
                for n in outputs:
                    self.determine_node_polarization(
                        n, self.graph, [], clk0, clk1, clk2, clk3
                    )

                # save output values
                for n in outputs:
                    print(
                        f"Saving value of component {n.value.get_name()}: {n.value.polarization}"
                    )
                    output_values[outputs.index(n)].append(n.value.polarization)

                # save values
                for n in self.graph.nodes:
                    cell_values[n.value.get_id()].append(n.value.polarization)

                # determine output values
                clk_values[0].append(clk0)
                clk_values[1].append(clk1)
                clk_values[2].append(clk2)
                clk_values[3].append(clk3)

            truth_table_values.append([n.value.polarization for n in outputs])

        num_subplots = len(inputs) + len(outputs) + 4

        # plot inputs
        for i in range(0, len(inputs)):
            plt.subplot(num_subplots, 1, i + 1)
            plt.title(inputs[i].value.label)
            plt.plot(input_values[i], color="blue")

        # plot outputs
        for i in range(0, len(outputs)):
            plt.subplot(num_subplots, 1, len(inputs) + i + 1)
            plt.title(outputs[i].value.label)
            plt.plot(output_values[i], color="yellow")

        # plot clock values
        for i in range(0, 4):
            plt.subplot(num_subplots, 1, len(inputs) + len(outputs) + i + 1)
            plt.title(f"clk{i}")
            plt.plot(clk_values[i], color="red")

        plt.show()

        truth_table = {}
        truth_table["inputs"] = [n.value.get_name() for n in inputs]
        truth_table["outputs"] = [n.value.get_name() for n in outputs]
        truth_table["values"] = truth_table_values
        return truth_table
