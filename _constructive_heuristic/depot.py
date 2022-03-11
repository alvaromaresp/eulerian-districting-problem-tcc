from typing import Dict
from .._abstracts._edge import _Edge
from .._abstracts._depot import _Depot

class Depot(_Depot):
    def __init__(self) -> None:
        self.border_edges : Dict[int, _Edge] = {}

    def addBorderEdge(self, edge: _Edge):
        self.border_edges.update({ edge.dst, edge })

        if (self.border_edges.has_key(edge.org)
            and (not self.border_edges.has_key(edge.dst))):

            self.border_edges.pop(edge.org)

