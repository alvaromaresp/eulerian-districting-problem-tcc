from typing import Dict
from edge import Edge

class Depot():
    def __init__(self, node) -> None:
        self.node = node
        self.edges : list[Edge] = []

    def addEdge(self, edge: Edge): 
        self.edges.append(edge)
        
