import random
from graph import Graph

def processFile(file, graph: Graph, num_depots: int) -> None:

    for line in file:
        processLine(line, graph)

    # for i in range(num_depots):
    #     node = graph.getNodeById(i + 1)
    #     graph.addDepot(node)

    graph.addDepot(graph.getNodeById(1))
    graph.addDepot(graph.getNodeById(graph.num_nodes - 1))

    colors = ["#"+''.join([random.choice('0123456789ABCDEF') for _ in range(num_depots)])
                    for _ in enumerate(graph.depots)]

    graph.setDepotColors(colors)
    graph.prepareData()

def processLine(line : str, graph: Graph):
    split = line.split(' ')

    getNodeNumber(split, graph)

    graph.buildEdgeFromLine(split)


def getNodeNumber(split, graph: Graph):
    if (split[0] == "NODES"):
        n_nodes = split[2].replace('\n','')
        graph.setNum_Nodes(int(n_nodes))

