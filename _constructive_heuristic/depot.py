import functools
import random
from typing import Dict

from node import Node
from edge import Edge
import time

class Depot():
    def __init__(self, initial_node : Node) -> None:
        self.initial_node = initial_node
        self.edges: list[Edge] = []
        self.border_edges : Dict[int, Edge] = {}
        self.total_demand : float = 0.0
        self.total_parity : float = 0.0
        self.nodes : list[Node] = []
        self.addInitialEdge()
        self.color = ''


    def addInitialEdge(self):
        self.nodes.append(self.initial_node)
        random_initial_edge = random.choice((self.nodes[0].edges))
        self.addBorderEdge(random_initial_edge)

    def addBorderEdge(self, edge: Edge):

        edge = self.addEdgeNodes(edge)

        self.total_demand = self.total_demand + edge.demand
        
        if (not self.border_edges):
            self.border_edges.update({ edge.org.id: edge })
        else:
            if (edge.org.id in self.border_edges):
                self.border_edges.update({ edge.dst.id: edge })

                if (not edge.org.doIHaveEdgesWithNoDistrict()):
                    self.border_edges.pop(edge.org.id)

            else:
                self.border_edges.update({ edge.org.id: edge })

                if (not edge.dst.doIHaveEdgesWithNoDistrict()):
                    self.border_edges.pop(edge.dst.id)

        print("Updating border with edge " + str(edge.id) + " with demand " + str(edge.demand))

    def addEdgeNodes(self, edge : Edge):
        node_id_list = list(map(lambda n: n.id, self.nodes))
        if edge.org.id not in node_id_list:
            self.nodes.append(edge.org)

        if edge.dst.id not in node_id_list:
            self.nodes.append(edge.dst)

        edge.depot_id = self.initial_node.id

        self.edges.append(edge)
        edge.org.updateNodeParityInDistrict()
        edge.dst.updateNodeParityInDistrict()

        return edge


    def updateBorder(self, edges: list[Edge]):
        print("Updating depot " + str(self.initial_node.id) + " with " + str(len(edges)) + " edges")
        for e in edges:
            self.addBorderEdge(e)

    def calculateParity(self, edges : list[Edge], node_num : int) -> float:
        total_parity = 0

        for node in self.nodes:
            total_parity = total_parity + node.district_parity.get(node_num)

        # REVISAR NÓ E ARESTAS NESTA FUNÇÃO
        return total_parity / len(self.nodes)

    def previewEdgeParity(self, edge : Edge):
        parity = 0
        for n in self.nodes:
            value = 0
            if (n.id == edge.org.id):
                value = edge.org.previewNodeParityInDistrict(self.node)
            elif (n.id == edge.dst.id):
                value = edge.dst.previewNodeParityInDistrict(self.node)
            else:
                value = n.district_parity.get(self.node)

            parity = parity + value

        return parity

    def updateParity(self):
        self.total_parity = self.calculateParity(self.edges, self.node)

    def canMyBorderIncrease(self):
        return functools.reduce(
            lambda acc, edge :
            acc or edge.dst.doIHaveEdgesWithNoDistrict() or edge.org.doIHaveEdgesWithNoDistrict()
        , self.border_edges.values(), False)

    
