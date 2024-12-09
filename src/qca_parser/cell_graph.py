from cell import Cell


class CellGraphConnection:
    def __init__(self, source: CellGraphNode, sink: CellGraphNode):
        self.source = source
        self.sink = sink


class CellGraphNode:
    def __init__(self, cell: Cell):
        self.connections: list[CellGraphConnection] = []
        self.value: Cell = cell

    def add_connection(self, connection: CellGraphConnection):
        self.connections.append(connection)


class CellGraph:
    def __init__(self):
        self.nodes = []

    def add_node(self, node: CellGraphNode):
        self.nodes.append(node)
