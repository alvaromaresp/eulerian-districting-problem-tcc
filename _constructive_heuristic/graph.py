from .._abstracts._graph import _Graph

class Graph(_Graph):

    G = nx.Graph()
    distance_matrix = []

    def __init__(self):
        self.n_nodes : int = None

    def addDepot(self, num_depots: int):
        pass

    def setN_Nodes(self, n_nodes: int):
        pass

    def setVehicles(self, n_nodes: int):
        pass

    def setDepotColors(self, n_nodes: int):
        pass

    def buildEdgeFromLine(self, string: str):
        pass
        ()
    def prepareData(self):
        pass
