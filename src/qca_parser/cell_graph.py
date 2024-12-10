from cell import Cell


class CellGraphNode:
    def __init__(self, cell: Cell):
        self.connections: list[CellGraphConnection] = []
        self.value: Cell = cell


class CellGraphConnection:
    def __init__(self, source: CellGraphNode, sink: CellGraphNode):
        self.source = source
        self.sink = sink


class CellGraph:
    def __init__(self):
        self.nodes = []
        self.connections = []

    def add_cell(self, cell: Cell):
        self.nodes.append(CellGraphNode(cell))

    def add_connection(self, source: CellGraphNode, sink: CellGraphNode):
        self.connections.append(CellGraphConnection(source, sink))
