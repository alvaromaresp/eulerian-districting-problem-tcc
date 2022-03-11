from .._abstracts._edge import _Edge
from .._abstracts._graph import _Graph
from node import Node
from .._abstracts._depot import _Depot

import functools
import networkx as nx
import matplotlib.pyplot  as plt

class Graph(_Graph):

    G = nx.Graph()
    distance_matrix = []

    def __init__(self):
        self.n_nodes : int = None
        self.vehicles : int = None
        self.depots : list[_Depot] = []
        self.capacity : int = None
        self.edges: list[_Edge] = []
        self.bigM : int = None

        self.node_degree : list[int] = []
        self.node_parity : list[int] = []

        self.nodes : list[Node] = []
        self.odd_degree_nodes : list[Node] = []
        self.even_degree_nodes : list[Node] = []

        self.depot_colors = []

    def addNode(self, node : Node):
        if node.id not in list(map(lambda n: n.id, self.nodes)):
            self.nodes.append(node)
        else:
            for i in self.nodes:
                if i.id == node.id:
                    for e in node.incident_edges:
                        i.addIncidentEdge(e)


    def addEdge(self, edge: _Edge):
        self.edges.append(edge)
        cost = 0
        if (edge.cost != 0):
            cost = edge.cost

        self.G.add_edge(edge.org, edge.dst, weight=cost)

    def setN_Nodes(self, n_nodes : int):
        self.n_nodes = n_nodes

    def setVehicles(self, vehicles : int):
        self.vehicles = vehicles

    def setCapacity(self, capacity : int):
        self.capacity = capacity

    def setBigM(self, bigM : int):
        self.bigM = bigM

    def addDepot(self, depot: int):
        self.depots.append(_Depot(depot))

    def addEdgeToDepotIndex(self, depot: int, edge : _Edge):
        self.depots[depot - 1].addEdge(edge)

    def setDepotColors(self, colors):
        self.depot_colors = colors

    def setNodeDegree(self):
        self.node_degree = [0] * self.n_nodes
        for e in self.edges:
            self.node_degree[e.org - 1] = self.node_degree[e.org - 1] + 1
            self.node_degree[e.dst - 1] = self.node_degree[e.dst - 1] + 1

        self.bigM = functools.reduce(lambda acc, actual : acc if acc > actual else actual, self.node_degree)

    def setNodeParity(self):
        if (len(self.node_degree) == 0) :
            self.setNodeDegree()

        self.node_parity = [0] * self.n_nodes

        for index, degree in enumerate(self.node_degree):
            self.node_parity[index] = 1 if degree % 2 == 0 else 0

        for node in self.nodes:
            if len(node.incident_edges) % 2 == 0:
                self.even_degree_nodes.append(node)
            else:
                self.odd_degree_nodes.append(node)

            node.degree = len(node.incident_edges)

    def printGraph(self, x_pe):

        pos = nx.spring_layout(self.G, seed=225)
        color_list = []

        for e, _ in enumerate(self.edges):
            color_list.append(self.getEdgeColorByDepot(x_pe, e))

        nx.draw(self.G, pos, edge_color = tuple(color_list), with_labels = True)
        plt.show()

    def getShortestPathEdgeLen(self, edge : _Edge, depot : _Depot):
        return min(self.distance_matrix[edge.org - 1][depot.node],
                   self.distance_matrix[edge.dst - 1][depot.node])

    def getEdgeColorByDepot(self, x_pe, edge):
        for p, _ in enumerate(self.depots):
            if x_pe[p][edge] == 1:
                return self.depot_colors[p]

    def setAllShortestPaths(self):
        self.distance_matrix = nx.floyd_warshall_numpy(self.G)

    def buildEdgeFromLine(self, split):
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

            edge = _Edge(
                len(self.edges),
                int(nodes[0]),
                int(nodes[1]),
                cost,
                demand
            )

            #Are we considering arcs?
            # org.addIncidentEdge(edge)
            dst.addIncidentEdge(edge)

            self.addNode(org)
            self.addNode(dst)
            self.addEdge(edge)

    def getIntValueFromTitle(self, line : list[str], title : str) -> int:
        value_index = line.index(title) + 1
        value = line[value_index]
        try :
            value = value.replace('\n', '')
            return int(value)
        except:
            return int(value)

    def prepareData(self):
        self.setNodeDegree()
        self.setNodeParity()
        self.setAllShortestPaths()