from typing import Dict

from node import Node
from .._abstracts._depot import _Depot
from edge import Edge

class Depot(_Depot):
    def __init__(self) -> None:
        self.border_edges : Dict[int, Edge] = {}
        self.total_demand : float = 0.0
        self.total_parity : float = 0.0
        self.nodes : list[Node] = []

    def addEdgeNodes(self, edge : Edge):
        if edge.org.id not in list(map(lambda n: n.id, self.nodes)):
            self.nodes.append(edge.org)

        if edge.dst.id not in list(map(lambda n: n.id, self.nodes)):
            self.nodes.append(edge.dst)

        edge.depot_id = self.node

        edge.org.updateEdgeDepot(edge)
        edge.dst.updateEdgeDepot(edge)

        return edge

    def addBorderEdge(self, edge: Edge):
        edge = self.addEdgeNodes(edge)

        self.border_edges.update({ edge.dst.id, edge })

        if (edge.org in self.border_edges
            and not edge.dst in self.border_edges):

            self.border_edges.pop(edge.org)

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
