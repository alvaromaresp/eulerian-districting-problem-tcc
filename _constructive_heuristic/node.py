import functools
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
        self.degree = self.degree + 1

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
                self.district_parity.update({ edge.depot_id: 0 if actual_parity == 1 else 1 })
            else:
                self.district_parity.update({ edge.depot_id: 0 })

    def doIHaveEdgesWithNoDistrict(self):
        return functools.reduce(
            lambda acc, edge :
            acc or edge.depot_id == -1
        , self.edges, True)
    
    
    def calculateLostParity(self):
        list_of_odd_districts = list(filter(lambda parity: parity == 1, self.district_parity.values()))
        if (self.degree % 2 == 0):
            return 1 if len(list_of_odd_districts) != 0 else 0
        else:
            return 1 if len(list_of_odd_districts) > 1 else 0
                
    def __str__(self):
        return "Node " + str(self.id) + " has " + str(self.degree) + " degrees"