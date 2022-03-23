import functools
from edge import Edge
from node import Node
from depot import Depot

import networkx as nx


class Graph():

    def __init__(self):
        self.depots : list[Depot] = []
        self.nodes : list[Node] = []
        self.d_ : float = 0
        self.num_nodes : int = None
        self.edges: list[Edge] = []
        self.G = nx.Graph()
        self.distance_matrix = []


    def setNum_Nodes(self, num_nodes: int):
        self.num_nodes = num_nodes

    def setDepotColors(self, colors):
        self.depot_colors = colors

    def getIntValueFromTitle(self, line : list[str], title : str) -> int:
        value_index = line.index(title) + 1
        value = line[value_index]
        try :
            value = value.replace('\n', '')
            return int(value)
        except:
            return int(value)


    def addEdge(self, edge: Edge):
        self.edges.append(edge)

        self.G.add_edge(edge.org, edge.dst)

    def setAllShortestPaths(self):
        self.distance_matrix = nx.floyd_warshall_numpy(self.G)

    def getShortestPathEdgeLen(self, edge : Edge, depot : int):
        return min(self.distance_matrix[edge.org.id - 1][depot],
                   self.distance_matrix[edge.dst.id - 1][depot])


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
            demand : int = 0

            for edge_info in split:
                if (edge_info == 'demand'):
                    demand = self.getIntValueFromTitle(split, edge_info)

            org = Node(int(nodes[0]) - 1)
            dst = Node(int(nodes[1]) - 1)

            edge = Edge(
                len(self.edges),
                org,
                dst,
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

    # def previewEdgeParityInDepots(self, edge : Edge, depot_id : int) -> float:
    #     return functools.reduce(lambda acc, actual :
    #         acc + actual.total_ if actual.depot_id != depot_id else acc + actual.total_demand + edge.demand
    #     , self.depots)

    def getNodeEdgesSortedByHeuristic(self, node : Node, depot : Depot) -> list[Edge]:
        return node.edges.sort(key= lambda edge :
            edge.demand + self.getShortestPathEdgeLen(edge, depot) +
            edge.org.previewNodeParityInDistrict(depot.node) # REFAZER ESTA PARTE
        )

    def getNodeEdgesSortedByDemandEquilibrium(self, node : Node, depot : Depot) -> list[Edge]:
        return node.edges.sort(key=self.previewEdgeDemandInDepots)


    def getNodeEdgesSortedByShortestPath(self, node : Node, depot : Depot)  -> list[Edge]:
        return node.edges.sort(key=lambda edge : self.getShortestPathEdgeLen(edge, depot))

    def setD_(self)  -> None:
        self.d_ = functools.reduce(lambda acc, actual :
            acc + actual.demand, self.edges, 0)
        self.d_ = self.d_ / len(self.depots)


    def areAllDemandsInsideD_Range(self, tau_1: float) -> bool:
        return functools.reduce(lambda acc, actual :
            acc and self.isDemandInsideLimits(actual, tau_1), self.depots, False)

    def isDemandInsideLimits(self, demand, tau_1):
        return demand <= self.d_ * (1 + tau_1) and demand >= self.d_ * (1 - tau_1)

    def isThereEdgeWithNoDistrict(self) -> bool:
        return -1 in list(map(lambda e: e.depot_id, self.edges))

    def getWorstNonBalancedDistrict(self, tau_1):
        if self.isThereEdgeWithNoDistrict():
            self.depots.sort(key=lambda d : d.total_demand)
        else:
            self.depots.sort(key=lambda d : -1 * self.d_ * (1 + tau_1) - d.total_demand)
        return self.depots[0]

    def getNodeById(self, node_id : int) -> Node:
        for n in self.nodes:
            if n.id == node_id:
                return n
        return None

    def prepareData(self):
        self.setAllShortestPaths()
        self.setD_()
