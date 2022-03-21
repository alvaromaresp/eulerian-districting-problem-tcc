from platform import node
from graph import Graph

from .._abstracts._data_processing import *
from .._abstracts._model import _Model

class ConstructiveModel(_Model):

    def execute(self, graph : Graph):

        k = 2
        
        while graph.isDemandBelowD_(self, 0.1):
            for depot in graph.depots:
                for (_, value) in depot.border_edges:
                    choosenEdges = graph.getNodeEdgesSortedByShortestPath(value.dst)
                    choosenEdges = choosenEdges[:k] if k <= value.dst.degree else choosenEdges[:value.dst.degree]
                    for e in choosenEdges:
                        depot.addBorderEdge(e)



    