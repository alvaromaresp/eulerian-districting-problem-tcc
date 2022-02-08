from edge import Edge
from node import Node
import functools

class Depot:
    def __init__(self, node) -> None:
        self.node = node
        self.edges : list[Edge] = []

    def addEdge(self, edge: Edge): 
        self.edges.append(edge)


class Graph:

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
        
    def addNode(self, node : Node):
        self.nodes.append(node)

    def addEdge(self, edge: Edge): 
        self.edges.append(edge)

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