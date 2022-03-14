from typing import Dict
from .._abstracts._node import _Node
from edge import Edge

class Node(_Node):
    def __init__(self):
        self.district_parity : Dict[int, int] = {}
        self.edges : list[Edge] = []

    def previewNodeParityInDistrict(self, depot_id : int):
        return 0 if self.district_parity.get(depot_id) == 1 else 0

    def updateEdgeDepot(self, edge : Edge):
        for e in self.edges:
            if (e.id == edge.id):
                e.depot_id = edge.depot_id
                break