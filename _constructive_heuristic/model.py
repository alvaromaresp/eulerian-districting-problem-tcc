import time
from graph import Graph
class ConstructiveModel():

    def execute(self, graph : Graph, chosen_execution = "heuristic"):

        k = 1
        tau_1 = 0.4

        while graph.areThereEdgesWithNoDistrict:
            try:
                depot = graph.getWorstNonBalancedDistrict(tau_1)
                choosenEdges = []
                for key in depot.border_edges:
                    if (chosen_execution == "heuristic"):
                        choosenEdges = choosenEdges + graph.getNodeEdgesSortedByHeuristic(depot.border_edges[key], depot.initial_node.id)
                    elif (chosen_execution == "demand"):
                        choosenEdges = choosenEdges + graph.getNodeEdgesSortedByDemand(depot.border_edges[key], depot.initial_node.id)
                    elif (chosen_execution == "objective"):
                        choosenEdges = choosenEdges + graph.getNodeEdgesSortedByObjectiveFuncion(depot.border_edges[key], depot.initial_node.id)

                if (k <= len(choosenEdges)):
                    depot.updateBorder(choosenEdges[:k])
                else:
                    depot.updateBorder(choosenEdges)
                    # depot.updateBorder(choosenEdges)
                graph.checklIfIfThereEdgeWithNoDistrict()
            except:
                graph.runDiagnostics(tau_1, depot)

        for d in graph.depots:
            print("DEMAND IN DEPOT " + str(d.initial_node.id) + " is " + str(d.total_demand))

        print("DEMAND MEAN = " + str(graph.d_))
        
        lost_parity = 0
        for n in graph.nodes:
            lost_parity = lost_parity + n.calculateLostParity()
            if (n.calculateLostParity() == 1):
                print("Node " + str(n.id) + " lost parity")

        print(str(lost_parity) + " nodes lost parity")

        graph.printGraph()
