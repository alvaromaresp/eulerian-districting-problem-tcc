from typing import Dict
from edge import Edge

class Node():
    def __init__(self, id):
        self.id : int = id
        self.edges : list[Edge] = []
        self.degree : int = 0
        self.district_parity : Dict[int, int] = {}

    def addEdge(self, edge : Edge):
        self.edges.append(edge)

    def previewNodeParityInDistrict(self, depot_id : int):
        return 0 if self.district_parity.get(depot_id) == 1 else 0

    def updateEdgeDepot(self, edge : Edge):
        for e in self.edges:
            if (e.id == edge.id):
                e.depot_id = edge.depot_id
                break
        self.updateNodeParityInDistrict()
        print("Node " + str(self.id) + " has parity " + str(self.district_parity.get(edge.depot_id)) + " in district " + str(edge.depot_id))

    def updateNodeParityInDistrict(self):
        self.district_parity.clear()
        for edge in self.edges:
            if edge.depot_id in self.district_parity:
                actual_parity = self.district_parity.get(edge.depot_id)
                self.district_parity.update({ edge.depot_id: actual_parity + 1 })
            else:
                self.district_parity.update({ edge.depot_id: 1 })
