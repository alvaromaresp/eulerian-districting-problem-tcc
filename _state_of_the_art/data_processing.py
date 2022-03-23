import random
from graph import Graph

class DataProcessing:
    def processFile(self, file, graph: Graph, num_depots: int) -> None:

        for line in file:
            self.processLine(line, graph)

        for i in range(num_depots):
            graph.addDepot(i)

        colors = ["#"+''.join([random.choice('0123456789ABCDEF') for _ in range(num_depots)])
                        for _ in enumerate(graph.depots)]

        graph.setDepotColors(colors)
        graph.prepareData()

    def processLine(self, line : str, graph: Graph):
        split = line.split(' ')

        self.getNodeNumber(split, graph)

        graph.buildEdgeFromLine(split)


    def getNodeNumber(self, split, graph: Graph):
        if (split[0] == "NODES"):
            n_nodes = split[2].replace('\n','')
            graph.setN_Nodes(int(n_nodes))

