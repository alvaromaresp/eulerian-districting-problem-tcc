import functools
import time

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
        self.highestDemand = -1
        self.highestDistance = -1

    def setNum_Nodes(self, num_nodes: int):
        self.num_nodes = num_nodes

    def setD_(self)  -> None:
        self.d_ = functools.reduce(lambda acc, actual :
            acc + actual.demand, self.edges, 0)
        self.d_ = self.d_ / len(self.depots)

    def setAllShortestPaths(self):
        self.distance_matrix = nx.floyd_warshall_numpy(self.G)


        for line in self.distance_matrix:
            for distance in line:
                if (distance > self.highestDistance):
                    self.highestDistance = distance

        print(self.highestDistance)


    def getNodeById(self, node_id : int) -> Node:
        for n in self.nodes:
            if n.id == node_id:
                return n
        return None

    def prepareData(self):
        self.setAllShortestPaths()
        self.setD_()

    def addDepot(self, initial_node: Node):
        self.depots.append(Depot(initial_node))

    def addNode(self, node : Node, edge : Edge):
        if node.id not in list(map(lambda n: n.id, self.nodes)):
            self.nodes.append(node)
        else:
            for i in self.nodes:
                if i.id == node.id:
                    for e in node.edges:
                        i.addEdge(e)

                    if i.id == edge.org.id:
                        edge.org = i
                    else:
                        edge.dst = i

    def addEdge(self, edge: Edge):
        edges = list(map(lambda e:  (e.org.id, e.dst.id), self.edges))
        edge_org_tuple = (edge.org.id, edge.dst.id)
        edge_dst_tuple = (edge.dst.id, edge.org.id)

        if ((not edge_org_tuple in edges) and (not edge_dst_tuple in edges)):
            edge.org.addEdge(edge)
            edge.dst.addEdge(edge)
            self.addNode(edge.org, edge)
            self.addNode(edge.dst, edge)
            self.edges.append(edge)

            self.G.add_edge(edge.org.id, edge.dst.id, weight=edge.weight)


    def getShortestPathEdgeLen(self, edge : Edge, depot : int):
        return min(nx.shortest_path_length(self.G, source=edge.org.id, target=depot, weight="weight"),
                    nx.shortest_path_length(self.G, source=edge.dst.id, target=depot, weight="weight"))

    def getCandidateEdges(self, edge : Edge) -> list[Edge]:
        candidateEdges = edge.org.edges + edge.dst.edges
        candidateEdges = list(filter(lambda e: e.depot_id == -1 and e.id != edge.id, candidateEdges))
        return candidateEdges

    def getNodeEdgesSortedByHeuristic(self, candidateEdges : list[Edge], depot_id : int)  -> list[Edge]:
        localCandidateEdges = list(filter(lambda e: e.depot_id == -1, candidateEdges))
        localCandidateEdges.sort(key=
            lambda e : self.getShortestPathEdgeLen(e, depot_id)/self.highestDistance - e.demand/self.highestDemand - e.previewNodesParityInDistrict(depot_id)/2)

        return candidateEdges

    def getNodeEdgesSortedByDemand(self, candidateEdges : list[Edge], depot_id : int)  -> list[Edge]:
        localCandidateEdges = list(filter(lambda e: e.depot_id == -1, candidateEdges))
        localCandidateEdges.sort(key=lambda e : e.demand, reverse=True)

        edgesWithEqualDemand = []
        for e in localCandidateEdges:
            if e.demand == localCandidateEdges[0].demand:
                edgesWithEqualDemand.append(e)

        if (len(edgesWithEqualDemand) > 1):
            edgesWithEqualDemand.sort(key = lambda e : self.getShortestPathEdgeLen(e, depot_id))
            return edgesWithEqualDemand


        return localCandidateEdges

    def getNodeEdgesSortedByObjectiveFuncion(self, candidateEdges : list[Edge], depot_id : int)  -> list[Edge]:
        localCandidateEdges = list(filter(lambda e: e.depot_id == -1, candidateEdges))
        localCandidateEdges.sort(key = lambda e : self.getShortestPathEdgeLen(e, depot_id))

        return localCandidateEdges

    def areAllDemandsInsideD_Range(self, tau_1: float) -> bool:
        return functools.reduce(lambda acc, actual :
            acc and self.isDemandInsideLimits(actual.total_demand, tau_1), self.depots, True)

    def isDemandInsideLimits(self, demand, tau_1):
        return demand <= self.d_ * (1 + tau_1) and demand >= self.d_ * (1 - tau_1)

    def checklIfIfThereEdgeWithNoDistrict(self) -> bool:
        self.areThereEdgesWithNoDistrict = -1 in list(map(lambda e: e.depot_id, self.edges))
        # print("There are edges with no district == " + str(self.areThereEdgesWithNoDistrict))

    def getWorstNonBalancedDistrict(self, tau_1):
        if not self.areAllDemandsInsideD_Range(tau_1):
            self.depots.sort(key=lambda d : d.total_demand)
        else:
            self.depots.sort(key=lambda d : self.d_ * (1 + tau_1) - d.total_demand, reverse=True) ## MAIOR DISTÂNCIA DO UPPER BOUND

        depots = list(filter(lambda d : d.canMyBorderIncrease(), self.depots))
        return depots[0]

    def printGraph(self):
        pos = nx.kamada_kawai_layout(self.G)

        for depot in self.depots:
            depot_edges = list(map(lambda e: (e.org.id, e.dst.id), depot.edges))
            nx.draw_networkx_edges(self.G, pos, depot_edges, edge_color= depot.color)

        edges_with_no_depot = list(map(lambda e:  (e.org.id, e.dst.id),filter(lambda e : e.depot_id == -1, self.edges)))
        nx.draw_networkx_edges(self.G, pos, edges_with_no_depot, edge_color= '#000000')
        nx.draw_networkx_nodes(self.G, pos)
        nx.draw_networkx_labels(self.G, pos)

        plt.show()

    def runDiagnostics(self, tau_1, actual_depot: Depot):
        print("Are all demands inside range? " + str(self.areAllDemandsInsideD_Range(tau_1)))
        print("Are there edges without districts? " + str(self.areThereEdgesWithNoDistrict))
        print("Depots demands: ")
        print(list(map(lambda d : d.total_demand, self.depots)))
        print("Depot chosen before exception: " + str(actual_depot.initial_node.id))

        self.printGraph()

    def depotsDistanceMean(self):
        depot_nodes_list = list(map(lambda d: d.initial_node.id, self.depots))
        total_distance = 0

        for d in depot_nodes_list:
            for i in range(depot_nodes_list.index(d) + 1, len(self.depots)):
                total_distance = total_distance + nx.shortest_path_length(self.G, source=d, target=depot_nodes_list[i], weight="weight")

        return total_distance/len(self.depots)