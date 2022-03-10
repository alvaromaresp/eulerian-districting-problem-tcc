from .._abstracts._graph import _Graph

class Graph(_Graph):

    G = nx.Graph()
    distance_matrix = []

    def __init__(self):
        self.n_nodes : int = None

    @abstractmethod
    def addDepot(self, num_depots: int):
        pass

    @abstractmethod
    def setN_Nodes(self, n_nodes: int):
        pass

    @abstractmethod
    def setVehicles(self, n_nodes: int):
        pass

    @abstractmethod
    def setDepotColors(self, n_nodes: int):
        pass

    @abstractmethod
    def buildEdgeFromLine(self, string: str):
        pass

    @abstractmethod()
    def prepareData(self):
        pass
