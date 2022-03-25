import time
from graph import Graph
class ConstructiveModel():

    def execute(self, graph : Graph):

        k = 2
        tau_1 = 0.1

        while not graph.areAllDemandsInsideD_Range(tau_1) and graph.isThereEdgeWithNoDistrict:
            depot = graph.getWorstNonBalancedDistrict(tau_1)
            choosenEdges = []
            for key in depot.border_edges:
                choosenEdges = choosenEdges + graph.getNodeEdgesSortedByShortestPathAndDemand(depot.border_edges[key].dst, depot)
                # choosenEdges = choosenEdges[:k] if k <= depot.border_edges[key].dst.degree else choosenEdges[:depot.border_edges[key].dst.degree]
                time.sleep(1)
            depot.updateBorder(choosenEdges)
            graph.checklIfIfThereEdgeWithNoDistrict()
            time.sleep(1)
            print("Updated depot " + str(depot.initial_node.id) + " now with demand " + str(depot.total_demand))
            print("Edges alocated = " + str(sum((len(d.edges)) for d in graph.depots)))