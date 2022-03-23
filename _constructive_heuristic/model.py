from graph import Graph
class ConstructiveModel():

    def execute(self, graph : Graph):

        k = 2
        tau_1 = 0.1

        while not graph.areAllDemandsInsideD_Range(tau_1) and graph.isThereEdgeWithNoDistrict():
            depot = graph.getWorstNonBalancedDistrict(tau_1)
            for key  in depot.border_edges:
                choosenEdges = graph.getNodeEdgesSortedByShortestPath(depot.border_edges[key].dst, depot.initial_node.id)
                choosenEdges = choosenEdges[:k] if k <= depot.border_edges[key].dst.degree else choosenEdges[:depot.border_edges[key].dst.degree]
                for e in choosenEdges:
                    depot.addBorderEdge(e)