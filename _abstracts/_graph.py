from abc import ABC, abstractmethod
from _depot import _Depot
from _node import _Node
from _edge import _Edge
import networkx as nx

class _Graph(ABC):

    def __init__(self):
        self.num_nodes : int = None
        self.edges: list[_Edge] = []
        self.G = nx.Graph()
        self.distance_matrix = []

    @abstractmethod
    def addDepot(self, num_depot: int):
        pass

    @abstractmethod
    def buildEdgeFromLine(self, string: str):
        pass

    @abstractmethod()
    def prepareData(self):
        pass


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


    def addEdge(self, edge: _Edge):
        self.edges.append(edge)
        cost = 0
        if (edge.cost != 0):
            cost = edge.cost

        self.G.add_edge(edge.org, edge.dst, weight=cost)

    def setAllShortestPaths(self):
        self.distance_matrix = nx.floyd_warshall_numpy(self.G)

    def getShortestPathEdgeLen(self, edge : _Edge, depot : _Depot):
        return min(self.distance_matrix[edge.org - 1][depot.node],
                   self.distance_matrix[edge.dst - 1][depot.node])
