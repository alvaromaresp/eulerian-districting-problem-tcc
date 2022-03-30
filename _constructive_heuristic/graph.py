import functools

from matplotlib import pyplot as plt
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
        self.areThereEdgesWithNoDistrict = True 

    def setNum_Nodes(self, num_nodes: int):
        self.num_nodes = num_nodes

    def setD_(self)  -> None:
        self.d_ = functools.reduce(lambda acc, actual :
            acc + actual.demand, self.edges, 0)
        self.d_ = self.d_ / len(self.depots)

    def setAllShortestPaths(self):
        self.distance_matrix = nx.floyd_warshall_numpy(self.G)

    def getNodeById(self, node_id : int) -> Node:
        for n in self.nodes:
            if n.id == node_id:
                return n
        return None

    def prepareData(self):
        self.setAllShortestPaths()
        self.setD_()

    def addDepot(self, num_depot: int):
        self.depots.append(Depot(num_depot))

    def addNode(self, node : Node):
        for e in node.edges:
            self.addEdge(e)
        if node.id not in list(map(lambda n: n.id, self.nodes)):
            self.nodes.append(node)
        else:
            for i in self.nodes:
                if i.id == node.id:
                    for e in node.edges:
                        i.addEdge(e)

    def addEdge(self, edge: Edge):
        # edges = list(map(lambda e:  (e.org.id, e.dst.id), self.edges))
        # edge_org_tuple = (edge.org.id, edge.dst.id)
        # edge_dst_tuple = (edge.dst.id, edge.org.id)

        # if ((not edge_org_tuple in edges) and (not edge_dst_tuple in edges)):
        self.edges.append(edge)

        self.G.add_edge(edge.org.id, edge.dst.id)


    def getShortestPathEdgeLen(self, edge : Edge, depot : int):
        # return nx.shortest_path_length(self.G, source=edge.dst.id, target=depot)
        return min(nx.shortest_path_length(self.G, source=edge.org.id, target=depot),
                    nx.shortest_path_length(self.G, source=edge.dst.id, target=depot))
        # return min(self.distance_matrix[edge.org.id - 1][depot],
        #            self.distance_matrix[edge.dst.id - 1][depot])

    def getShortestPathNodeLen(self, node : Node, depot : int):
        return nx.shortest_path_length(self.G, source=node.id, target=depot)

    # def previewEdgeDemandInDepots(self, edge : Edge, depot_id : int) -> float:
    #     return functools.reduce(lambda acc, actual :
    #         acc + actual.total_demand if actual.depot_id != depot_id else acc + actual.total_demand + edge.demand
    #     , self.depots)

    # def previewEdgeParityInDepots(self, edge : Edge, depot_id : int) -> float:
    #     return functools.reduce(lambda acc, actual :
    #         acc + actual.total_ if actual.depot_id != depot_id else acc + actual.total_demand + edge.demand
    #     , self.depots)

    # def getNodeEdgesSortedByHeuristic(self, node : Node, depot : Depot) -> list[Edge]:
    #     node.edges.sort(key= lambda edge :
    #         edge.demand + self.getShortestPathEdgeLen(edge, depot) +
    #         edge.org.previewNodeParityInDistrict(depot.node) # REFAZER ESTA PARTE
    #     )
    #     return node.edges

    # def getNodeEdgesSortedByDemandEquilibrium(self, node : Node, depot : Depot) -> list[Edge]:
    #     node.edges.sort(key=self.previewEdgeDemandInDepots)
    #     return node.edges

    def getNodeEdgesSortedByShortestPath(self, node : Node, depot : Depot)  -> list[Edge]:
        node.edges.sort(key=lambda edge : self.getShortestPathEdgeLen(edge, depot.initial_node.id))
        return node.edges

    def getNodeEdgesSortedByShortestPathAndDemand(self, edge : Edge, depot_id : int)  -> list[Edge]:
        # NORMALIZAR
        print("Chosen edge: " + str(edge.id))
        candidateEdges = edge.org.edges + edge.dst.edges
        candidateEdges.sort(key=lambda e : self.getShortestPathEdgeLen(e, depot_id) - edge.demand)

        candidateEdges = list(filter(lambda e: e.id != edge.id, candidateEdges))
        
        print("Candidate edges length: " + str(len(candidateEdges)))
        if self.areThereEdgesWithNoDistrict:
            candidateEdges = list(filter(lambda e: e.depot_id == -1, candidateEdges))
            print("Candidate edges length if there is edges with no district: " + str(len(candidateEdges)))
        else:
            candidateEdges = list(filter(lambda e: e.depot_id == depot_id, candidateEdges))
            print("Candidate edges length if there is no edges with no district: " + str(len(candidateEdges)))
        return candidateEdges


    def areAllDemandsInsideD_Range(self, tau_1: float) -> bool:
        return functools.reduce(lambda acc, actual :
            acc and self.isDemandInsideLimits(actual.total_demand, tau_1), self.depots, True)

    def isDemandInsideLimits(self, demand, tau_1):
        return demand <= self.d_ * (1 + tau_1) and demand >= self.d_ * (1 - tau_1)

    def checklIfIfThereEdgeWithNoDistrict(self) -> bool:
        self.areThereEdgesWithNoDistrict = -1 in list(map(lambda e: e.depot_id, self.edges))
        print("There are edges with no district == " + str(self.areThereEdgesWithNoDistrict))

    def getWorstNonBalancedDistrict(self, tau_1):
        depots = list(filter(lambda d : d.canMyBorderIncrease(), self.depots))
        depots = self.depots if len(depots) == 0 else depots
        if self.areThereEdgesWithNoDistrict:
            depots.sort(key=lambda d : d.total_demand)
        else:
            depots.sort(key=lambda d : -1 * self.d_ * (1 + tau_1) - d.total_demand) ## VERIFICAR LAMBDA
        return depots[0]

    def printGraph(self):
        pos = nx.spring_layout(self.G, seed=225)



        for depot in self.depots:
            depot_edges = list(map(lambda e: (e.org.id, e.dst.id), depot.edges))
            print(depot_edges)
            nx.draw_networkx_edges(self.G, pos, depot_edges, edge_color= depot.color)

        # for e in edges:
        #     print(e)

        edges = list(map(lambda e:  (e.org.id, e.dst.id),filter(lambda e : e.depot_id == -1, self.edges)))
        print(edges)
        nx.draw_networkx_edges(self.G, pos, edges, edge_color= '#000000')
        nx.draw_networkx_nodes(self.G, pos)
        nx.draw_networkx_labels(self.G, pos)

        plt.show()

    def getEdgeColorByDepot(self, edge: Edge):
        if edge.depot_id == -1:
            return 'b'

        for depot in self.depots:
            if edge.depot_id == depot.initial_node.id:
                return depot.color
