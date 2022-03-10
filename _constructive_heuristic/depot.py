from typing import Dict
from edge import Edge


class Depot():
    def __init__(self, node) -> None:
        self.node = node
        self.border_edges : Dict[int, Edge] = {}

    def addBorderEdge(self, edge: Edge):
        self.border_edges.update({ edge.dst, edge })
        
        if (self.border_edges.has_key(edge.org) 
            and (not self.border_edges.has_key(edge.dst))):

            self.border_edges.pop(edge.org)
        
