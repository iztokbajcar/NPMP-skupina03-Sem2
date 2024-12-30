from component import Component
from cell import Cell
from gate import Gate, GateType
from majority_gate import MajorityGate
from negator import Negator
from utils import euclidean_dist, manhattan_dist
import math


class GraphNode:
    def __init__(self, component: Component):
        self.connections: list[GraphConnection] = []
        self.value: Component = component


class GraphConnection:
    def __init__(self, source: GraphNode, sink: GraphNode):
        self.source = source
        self.sink = sink


class Graph:
    def __init__(self):
        self.nodes = []
        self.connections = []

    def add_component(self, component: Component) -> GraphNode:
        node = GraphNode(component)
        self.nodes.append(node)
        return node

    def add_connection(self, source: GraphNode, sink: GraphNode):
        self.connections.append(GraphConnection(source, sink))

    def remove_component(self, component: Component):
        for n in self.nodes:
            if n.value == component:
                self.nodes.remove(n)

                to_remove = []
                for c in self.connections:
                    if c.source == n or c.sink == n:
                        print(
                            f"Removing connection {c.source.value.get_name()} -> {c.sink.value.get_name()}"
                        )
                        to_remove.append(c)

                for c in to_remove:
                    self.connections.remove(c)
                return

    def remove_connection(self, source: GraphNode, sink: GraphNode):
        for c in self.connections:
            if c.source == source and c.sink == sink:
                self.connections.remove(c)
                return

        # raise Exception("Connection not found")

    def component_neighbors(self, component: Component) -> list[Component]:
        """Returns the neighbors of the given cell."""
        neighbors = []

        for conn in self.connections:
            if conn.source.value == component:
                neighbors.append(conn.sink)

        return neighbors

    def recognize_structures(self) -> None:
        # TODO: prettify this
        for node1 in self.nodes:
            if type(node1.value) is not Cell:
                continue

            cell1 = node1.value
            # neigh1 = [
            #     n for n in self.component_neighbors(cell1) if isinstance(n.value, Cell)
            # ]
            neigh1 = self.component_neighbors(cell1)

            # if the node has 4 neighbors (not counting diagonals),
            # they form a majority gate
            von_neumann_neighbors = [
                n
                for n in neigh1
                if isinstance(n.value, Cell)
                and manhattan_dist((cell1.x, cell1.y), (n.value.x, n.value.y)) == 1
            ]
            if len(von_neumann_neighbors) == 4:
                print(f"MAJ between {cell1.get_name()}")
                print(f"    - neighbors: {[n.value.get_name() for n in neigh1]}")
                print(
                    f"    - von Neumann neighbors: {[n.value.get_name() for n in von_neumann_neighbors]}"
                )
                maj = self.add_component(
                    MajorityGate(
                        f"{cell1.get_id()}+{'+'.join([n.value.get_id() for n in von_neumann_neighbors])}"
                    )
                )

                # replace the center cell with the majority gate
                for n in von_neumann_neighbors:
                    self.add_connection(n, maj)
                    self.add_connection(maj, n)
                self.remove_component(cell1)

                # remove diagonal connections between outer cells
                for n1 in von_neumann_neighbors:
                    for n2 in von_neumann_neighbors:
                        if n1 == n2:
                            continue
                        self.remove_connection(n1, n2)
                        self.remove_connection(n2, n1)

                continue

            for node2 in self.nodes:
                if type(node2.value) is not Cell:
                    continue

                cell2 = node2.value
                # neigh2 = [
                #     n
                #     for n in self.component_neighbors(cell2)
                #     if isinstance(n.value, Cell)
                # ]
                neigh2 = self.component_neighbors(cell2)

                e_dist = euclidean_dist((cell1.x, cell1.y), (cell2.x, cell2.y))

                common_neigh = [c for c in neigh1 if c in neigh2]

                if (
                    math.isclose(e_dist, math.sqrt(2))
                    and cell1.get_id() < cell2.get_id()
                    and len(common_neigh) == 0
                ):
                    # assumption: if the cells are diagonally adjacent and
                    # have no common neighbors, they form a negator
                    print(f"NEG between {cell1.get_name()} and {cell2.get_name()}")
                    print(f"    - neigh1: {[n.value.get_name() for n in neigh1]}")
                    print(f"    - neigh2: {[n.value.get_name() for n in neigh2]}")
                    print(
                        f"    - common neighbors: {[n.value.get_name() for n in common_neigh]}"
                    )
                    negator = self.add_component(
                        Negator(f"{cell1.get_id()}+{cell2.get_id()}")
                    )

                    # remove old connection
                    self.remove_connection(node1, node2)
                    self.remove_connection(node2, node1)

                    # add new connections
                    self.add_connection(node1, negator)
                    self.add_connection(negator, node1)
                    self.add_connection(node2, negator)
                    self.add_connection(negator, node2)
