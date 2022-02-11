from edge import Edge
from node import Node

import functools
import networkx as nx 
import matplotlib.pyplot  as plt

class Depot:
    def __init__(self, node) -> None:
        self.node = node
        self.edges : list[Edge] = []

    def addEdge(self, edge: Edge): 
        self.edges.append(edge)


class Graph:

    G = nx.Graph()

    def __init__(self):
        self.n_nodes : int = None
        self.vehicles : int = None
        self.depots : list[Depot] = []
        self.capacity : int = None
        self.edges: list[Edge] = []
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
                    

    def addEdge(self, edge: Edge): 
        self.edges.append(edge)
        self.G.add_edge(edge.org, edge.dst)

    def setN_Nodes(self, n_nodes : int):
        self.n_nodes = n_nodes
    
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

    def getShortestPathLen(self, org, dst):
        return len(nx.shortest_path(self.G, org, dst)) - 2
    
    def getShortestPathEdgeLen(self, edge : Edge, depot : Depot):
        return min(self.getShortestPathLen(edge.org, depot.node),
                   self.getShortestPathLen(edge.dst, depot.node))

    def getEdgeColorByDepot(self, x_pe, edge):
        for p, _ in enumerate(self.depots):
            if x_pe[p][edge] == 1:
                return self.depot_colors[p]