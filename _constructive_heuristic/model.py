from platform import node
from graph import Graph

from .._abstracts._data_processing import *
from .._abstracts._model import _Model

class ConstructiveModel(_Model):

    def execute(self, graph : Graph):

        k = 2
        tau_1 = 0.1

        while graph.areAllDemandsInsideD_Range(tau_1) and graph.isThereEdgeWithNoDistrict():
            depot = graph.getWorstNonBalancedDistrict(tau_1)
            for (_, value) in depot.border_edges:
                choosenEdges = graph.getNodeEdgesSortedByShortestPath(value.dst)
                choosenEdges = choosenEdges[:k] if k <= value.dst.degree else choosenEdges[:value.dst.degree]
                for e in choosenEdges:
                    depot.addBorderEdge(e)