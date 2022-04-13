import random
from edge import Edge
from node import Node
from graph import Graph

def processFile(file, graph: Graph, num_depots: int = 3) -> None:

    for line in file:
        processLine(line, graph)

    for i in range(num_depots):
        graph.addDepot(i)

    colors = ["#"+''.join([random.choice('0123456789ABCDEF') for _ in range(6)])
                    for _ in enumerate(graph.depots)]

    graph.setDepotColors(colors)
    prepareData(graph)

def processLine(line : str, graph: Graph):
    split = line.split(' ')

    getNodeNumber(split, graph)

    buildEdgeFromLine(graph, split)


def getNodeNumber(split, graph: Graph):
    if (split[0] == "NODES"):
        n_nodes = split[2].replace('\n','')
        graph.setNum_Nodes(int(n_nodes))

def getIntValueFromTitle(line : list[str], title : str) -> int:
    value_index = line.index(title) + 1
    value = line[value_index]
    try :
        value = value.replace('\n', '')
        return int(value)
    except:
        return int(value)


def buildEdgeFromLine(graph: Graph, split):
    if (split[0][0] == '('):
        nodes = split[0][1:-1].split(',')
        demand : int = 0

        for edge_info in split:
            if (edge_info =='demand'):
                demand = getIntValueFromTitle(split, edge_info)

        edge = Edge(
            len(graph.edges),
            int(nodes[0]),
            int(nodes[1]),
            demand
        )

        graph.addEdge(edge)


def prepareData(graph: Graph):
    graph.setNodeDegree()
    graph.setNodeParity()
    graph.setAllShortestPaths()