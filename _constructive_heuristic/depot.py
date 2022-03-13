from typing import Dict
from .._abstracts._edge import _Edge
from .._abstracts._depot import _Depot
from edge import Edge

class Depot(_Depot):
    def __init__(self) -> None:
        self.border_edges : Dict[int, Edge] = {}
        self.total_demand : float = 0.0
        self.total_parity : float = 0.0

    
    
    def addBorderEdge(self, edge: Edge):
        self.border_edges.update({ edge.dst, edge })

        if (edge.org in self.border_edges
            and not edge.dst in self.border_edges):

            self.border_edges.pop(edge.org)

    def calculateParity(self, edges : list[Edge]) -> float:
        total_parity = 0
        for edge in edges:
            if (len(edge.org) % 2 == 0):
                total_parity = total_parity + 1
        
        return total_parity / len(edge)

    def previewEdgeParity(self, edge):
        tempEdges = self.edges + edge

    def updateParity(self):
        self.total_parity = self.calculateParity(self.edges)
