from edge import Edge
from node import Node
from depot import Depot

import functools
import networkx as nx
import matplotlib.pyplot  as plt

class Graph():

    def __init__(self):
        self.num_nodes : int = None
        self.edges: list[Edge] = []
        self.G = nx.Graph()
        self.distance_matrix = []
        self.vehicles : int = None
        self.depots : list[Depot] = []
        self.capacity : int = None
        self.bigM : int = None

        self.node_degree : list[int] = []
        self.node_parity : list[int] = []

        self.nodes : list[Node] = []
        self.odd_degree_nodes : list[Node] = []
        self.even_degree_nodes : list[Node] = []

        self.depot_colors = []


    def setNum_Nodes(self, num_nodes: int):
        self.num_nodes = num_nodes

    def setDepotColors(self, colors):
        self.depot_colors = colors

    def addEdge(self, edge: Edge):
        edges = list(map(lambda e:  (e.org, e.dst), self.edges))
        edge_org_tuple = (edge.org, edge.dst)
        edge_dst_tuple = (edge.dst, edge.org)

        if ((not edge_org_tuple in edges) and (not edge_dst_tuple in edges)):
            org = Node(edge.org - 1)
            dst = Node(edge.dst - 1)
            org.addEdge(edge)
            dst.addEdge(edge)
            self.addNode(org)
            self.addNode(dst)
            self.edges.append(edge)

            self.G.add_edge(org.id, dst.id)

    def setAllShortestPaths(self):
        self.distance_matrix = nx.floyd_warshall_numpy(self.G)

    def getShortestPathEdgeLen(self, edge : Edge, depot : Depot):
        return min(nx.shortest_path_length(self.G, source=edge.org - 1, target=depot.node),
                    nx.shortest_path_length(self.G, source=edge.dst - 1, target=depot.node))

    def addNode(self, node : Node):
        if node.id not in list(map(lambda n: n.id, self.nodes)):
            self.nodes.append(node)
        else:
            for i in self.nodes:
                if i.id == node.id:
                    for e in node.edges:
                        i.addEdge(e)

    def setVehicles(self, vehicles : int):
        self.vehicles = vehicles

    def setCapacity(self, capacity : int):
        self.capacity = capacity

    def setBigM(self, bigM : int):
        self.bigM = bigM

    def addDepot(self, depot: int):
        self.depots.append(Depot(depot))

    def addEdgeToDepotIndex(self, depot: int, edge : Edge):
        self.depots[depot - 1].addEdge(edge)

    def setNodeDegree(self):
        self.node_degree = [0] * self.num_nodes
        for e in self.edges:
            self.node_degree[e.org - 1] = self.node_degree[e.org - 1] + 1
            self.node_degree[e.dst - 1] = self.node_degree[e.dst - 1] + 1

        self.bigM = functools.reduce(lambda acc, actual : acc if acc > actual else actual, self.node_degree, -1)

    def setNodeParity(self):
        if (len(self.node_degree) == 0) :
            self.setNodeDegree()

        self.node_parity = [0] * self.num_nodes

        for index, degree in enumerate(self.node_degree):
            self.node_parity[index] = 1 if degree % 2 == 0 else 0

        for node in self.nodes:
            if len(node.edges) % 2 == 0:
                self.even_degree_nodes.append(node)
            else:
                self.odd_degree_nodes.append(node)

    def printGraph(self, x_pe):

        pos = nx.spring_layout(self.G, seed=225)
        color_list = []

        for e, _ in enumerate(self.edges):
            color_list.append(self.getEdgeColorByDepot(x_pe, e))

        nx.draw(self.G, pos, edge_color = tuple(color_list), with_labels = True)
        plt.show()


    def getEdgeColorByDepot(self, x_pe, edge):
        for p, _ in enumerate(self.depots):
            if x_pe[p][edge] == 1:
                return self.depot_colors[p]