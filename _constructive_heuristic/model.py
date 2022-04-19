import time
from graph import Graph
class ConstructiveModel():

    def execute(self, graph : Graph, chosen_execution = "heuristic", k = 1, tau_1 = 0.4):

        start_time = time.time()
        while graph.areThereEdgesWithNoDistrict:
            try:
                depot = graph.getWorstNonBalancedDistrict(tau_1)
                choosenEdges = []
                for key in depot.border_edges:
                    choosenEdges = choosenEdges + graph.getCandidateEdges(depot.border_edges[key])

                if (chosen_execution == "heuristic"):
                    choosenEdges = graph.getNodeEdgesSortedByHeuristic(choosenEdges, depot.initial_node.id)
                elif (chosen_execution == "demand"):
                    choosenEdges = graph.getNodeEdgesSortedByDemand(choosenEdges, depot.initial_node.id)
                elif (chosen_execution == "objective"):
                    choosenEdges = graph.getNodeEdgesSortedByObjectiveFuncion(choosenEdges, depot.initial_node.id)

                if (k <= len(choosenEdges)):
                    depot.updateBorder(choosenEdges[:k])
                else:
                    depot.updateBorder(choosenEdges)
                graph.checklIfIfThereEdgeWithNoDistrict()
            except:
                graph.runDiagnostics(tau_1, depot)

        execution_time = time.time() - start_time

        for d in graph.depots:
            print("DEMAND IN DEPOT " + str(d.initial_node.id) + " is " + str(d.total_demand))

        print("DEMAND MEAN = " + str(graph.d_))

        lost_parity = 0
        for n in graph.nodes:
            lost_parity = lost_parity + n.calculateLostParity()

        print(str(lost_parity) + " nodes lost parity")


        objective_function = 0

        for d in graph.depots:
            for e in d.edges:
                objective_function = objective_function + graph.getShortestPathEdgeLen(e, d.initial_node.id)

        print("Objective function: " + str(objective_function))

        print("Depot distance mean: " + str(graph.depotsDistanceMean()))

        # graph.printGraph()

        return (lost_parity/len(graph.nodes), objective_function, graph.depotsDistanceMean(), execution_time)
