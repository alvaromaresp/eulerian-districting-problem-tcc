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
        self.edges.append(random_initial_edge)
        self.border_edges.update({ random_initial_edge.dst.id:  random_initial_edge})
        self.border_edges.update({ random_initial_edge.org.id:  random_initial_edge})

    def addEdgeNodes(self, edge : Edge):
        node_id_list = list(map(lambda n: n.id, self.nodes))
        if edge.org.id not in node_id_list:
            print("Adding origin node " + str(edge.org.id))
            self.nodes.append(edge.org)

        if edge.dst.id not in node_id_list:
            print("Adding destination node " + str(edge.dst.id))
            self.nodes.append(edge.dst)

        edge.depot_id = self.initial_node.id

        edge.org.updateEdgeDepot(edge)
        edge.dst.updateEdgeDepot(edge)
        self.edges.append(edge)

        return edge

    def addBorderEdge(self, edge: Edge):
        # BORDA TEM APENAS VÉRTICES COM ARESTAS NÃO SELECIONADAS OU ARESTAS FRONTEIRIÇAS

        edge = self.addEdgeNodes(edge)

        self.total_demand = self.total_demand + edge.demand

        self.border_edges.update({ edge.dst.id: edge })
        self.border_edges.update({ edge.org.id: edge })
        print("Updating border with edge " + str(edge.id) + " with demand " + str(edge.demand))
        time.sleep(1)
        if (edge.org in self.border_edges
            and not edge.dst in self.border_edges):

            self.border_edges.pop(edge.org)

    def updateBorder(self, edges: list[Edge]):
        print("Number of edges selected = " + str(len(edges)))
        time.sleep(1)
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

    
