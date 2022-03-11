from typing import Dict
from _edge import _Edge

class _Depot():
    def __init__(self, node) -> None:
        self.node = node
        self.edges : list[_Edge] = []

    def addEdge(self, edge: _Edge):
        self.edges.append(edge)

