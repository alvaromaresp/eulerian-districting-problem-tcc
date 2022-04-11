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
        return 1 if depot_id in self.district_parity and self.district_parity.get(depot_id) == 0 else 0

    def setParityInDistrict(self, depot_id : int):
        if depot_id in self.district_parity and self.district_parity.get(depot_id) == 0:
            self.district_parity.update({ depot_id: 1 })
        else:
            self.district_parity.update({ depot_id: 0 })

    def getParityInDistrict(self, depot_id : int):
        if depot_id in self.district_parity:
            return self.district_parity.get(depot_id)
        else:
            return 0

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
        , self.edges, False)
    
    
    def calculateLostParity(self):
        list_of_odd_districts = list(filter(lambda parity: parity == 0, self.district_parity.values()))
        if (self.degree % 2 == 0):
            return 1 if len(list_of_odd_districts) != 0 else 0
        else:
            return 1 if len(list_of_odd_districts) > 1 else 0
                
    def __str__(self):
        return "Node " + str(self.id) + " has " + str(self.degree) + " degrees"