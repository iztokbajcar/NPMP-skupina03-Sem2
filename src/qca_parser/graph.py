from component import Component
from cell import Cell
from gate import Gate, GateType
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

    def remove_connection(self, source: GraphNode, sink: GraphNode):
        for c in self.connections:
            if c.source == source and c.sink == sink:
                self.connections.remove(c)
                return

        raise Exception("Connection not found")

    def component_neighbors(self, component: Component) -> list[Component]:
        """Returns the neighbors of the given cell."""
        neighbors = []

        for conn in self.connections:
            if conn.source.value == component:
                neighbors.append(conn.sink)

        return neighbors

    def recognize_structures(self) -> None:
        for node1 in self.nodes:
            if type(node1.value) is not Cell:
                continue

            cell1 = node1.value
            for node2 in self.nodes:
                if type(node2.value) is not Cell:
                    continue

                cell2 = node2.value

                e_dist = euclidean_dist((cell1.x, cell1.y), (cell2.x, cell2.y))
                neigh1 = self.component_neighbors(cell1)
                neigh2 = self.component_neighbors(cell2)
                common_neigh = [
                    c for c in neigh1 if c in neigh2 and isinstance(c.value, Cell)
                ]

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
