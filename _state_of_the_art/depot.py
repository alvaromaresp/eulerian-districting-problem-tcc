from edge import Edge

class Depot():
    def __init__(self, node : int) -> None:
        self.node : int = node
        self.edges : list[Edge] = []

    def addEdge(self, edge: Edge):
        self.edges.append(edge)

