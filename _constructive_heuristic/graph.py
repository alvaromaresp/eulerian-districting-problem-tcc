import functools
from edge import Edge
from .._abstracts._graph import _Graph
from node import Node
from depot import Depot

import networkx as nx
import matplotlib.pyplot  as plt


class Graph(_Graph):

    def __init__(self):
        self.depots : list[Depot] = []
        self.nodes : list[Node] = []
        
    def addDepot(self, num_depot: int):
        self.depots.append(Depot(num_depot))

    def addNode(self, node : Node):
        if node.id not in list(map(lambda n: n.id, self.nodes)):
            self.nodes.append(node)
        else:
            for i in self.nodes:
                if i.id == node.id:
                    for e in node.edges:
                        i.addEdge(e)

    def buildEdgeFromLine(self, split: str):
        if (split[0][0] == '('):
            nodes = split[0][1:-1].split(',')
            cost : int = None
            demand : int = 0

            for edge_info in split:
                if (edge_info == 'trav_cost' or edge_info == 'cost'):
                    cost = self.getIntValueFromTitle(split, edge_info)
                if (edge_info == 'demand'):
                    demand = self.getIntValueFromTitle(split, edge_info)

            org = Node(int(nodes[0]) - 1)
            dst = Node(int(nodes[1]) - 1)

            edge = Edge(
                len(self.edges),
                int(nodes[0]),
                int(nodes[1]),
                cost,
                demand
            )

            org.addEdge(edge)
            dst.addEdge(edge)

            self.addNode(org)
            self.addNode(dst)
            self.addEdge(edge)

    def previewEdgeDemandInDepots(self, edge : Edge, depot_id : int) -> float:
        return functools.reduce(lambda acc, actual :
            acc + actual.total_demand if actual.depot_id != depot_id else acc + actual.total_demand + edge.demand
        , self.depots)

    def previewEdgeParityInDepots(self, edge : Edge, depot_id : int) -> float:
        return functools.reduce(lambda acc, actual :
            acc + actual.total_ if actual.depot_id != depot_id else acc + actual.total_demand + edge.demand
        , self.depots)     

    def getNodeEdgesSortedByHeuristic(self, node : Node, depot : Depot) -> list[Edge]:
        return node.edges.sort(key= lambda edge :
            edge.demand + self.getShortestPathEdgeLen(edge, depot) +
            edge.org.previewNodeParityInDistrict(depot.node)
        )

    def getNodeEdgesSortedByDemandEquilibrium(self, node : Node, depot : Depot) -> list[Edge]:
        return node.edges.sort(key=self.previewEdgeDemandInDepots)


    def getNodeEdgesSortedByObjetiveFunction(self, node : Node, depot : Depot)  -> list[Edge]:
        return node.edges.sort(lambda edge : self.getShortestPathEdgeLen(edge, depot))

    def prepareData(self):
        pass
