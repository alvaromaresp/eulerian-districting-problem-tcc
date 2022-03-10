import random
from .._abstracts._graph import _Graph

def processFile(file, graph: _Graph, num_depots: int) -> None:

    for line in file:
        processLine(line, graph)

    for i in range(num_depots):
        graph.addDepot(i)
    
    colors = ["#"+''.join([random.choice('0123456789ABCDEF') for _ in range(num_depots)])
                    for _ in enumerate(graph.depots)]

    graph.setDepotColors(colors)
    graph.prepareData()

def processLine(line : str, graph: _Graph):
    split = line.split(' ')
    
    getNodeNumber(split, graph)

    graph.buildEdgeFromLine(split)


def getNodeNumber(split, graph: _Graph):
    if (split[0] == "NODES"):
        n_nodes = split[2].replace('\n','')
        graph.setN_Nodes(int(n_nodes))

