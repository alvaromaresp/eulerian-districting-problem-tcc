import time
from graph import Graph
class ConstructiveModel():

    def execute(self, graph : Graph):

        k = 2
        tau_1 = 0.4

        # MELHORAR CRITÉRIO DE PARADA PARA NÃO ENTRAR EM LOOP DE DISPUTA DE ARESTAS
        while graph.areThereEdgesWithNoDistrict:
            graph.printGraph()
            depot = graph.getWorstNonBalancedDistrict(tau_1)
            if depot == None:
                break
            choosenEdges = []
            print("Chosen depot: " + str(depot.initial_node.id))
            for key in depot.border_edges:
                choosenEdges = choosenEdges + graph.getNodeEdgesSortedByShortestPathAndDemand(depot.border_edges[key], depot.initial_node.id)
                #time.sleep(1)
            # depot.updateBorder(choosenEdges)
            depot.addBorderEdge(choosenEdges[0])
            graph.checklIfIfThereEdgeWithNoDistrict()
            #time.sleep(1)
            print("Updated depot " + str(depot.initial_node.id) + " now with demand " + str(depot.total_demand))
            print("Edges alocated = " + str(sum((len(d.edges)) for d in graph.depots)))

            for n in graph.nodes:
                n.updateNodeParityInDistrict()

        for d in graph.depots:
            print("DEMAND IN DEPOT " + str(d.initial_node.id) + " is " + str(d.total_demand))

        print("DEMAND MEAN = " + str(graph.d_))
        
        lost_parity = 0
        for n in graph.nodes:
            lost_parity = lost_parity + n.calculateLostParity()

        print(str(lost_parity) + " nodes lost parity")

        graph.printGraph()
        print(graph.areThereEdgesWithNoDistrict)
