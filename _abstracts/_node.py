from .._abstracts._edge import _Edge

class _Node:
    def __init__(self, id):
        self.id : int = id
        self.edges : list[_Edge] = []
        self.degree : int = 0

    def addEdge(self, edge : _Edge):
        self.edges.append(edge)

