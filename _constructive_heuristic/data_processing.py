import random
from edge import Edge
from node import Node
from graph import Graph

def processFile(file, graph: Graph, num_depots: int) -> None:

    for line in file:
        processLine(line, graph)

    # for i in range(num_depots):
    #     node = graph.getNodeById(i + 1)
    #     graph.addDepot(node)


    graph.addDepot(graph.getNodeById(1))
    graph.addDepot(graph.getNodeById(graph.num_nodes - 1))

    setDepotColors(graph)

    graph.prepareData()

def processLine(line : str, graph: Graph):
    split = line.split(' ')

    getNodeNumber(split, graph)

    buildEdgeFromLine(split, graph)


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

def buildEdgeFromLine(split: str, graph : Graph):
    if (split[0][0] == '('):
        nodes = split[0][1:-1].split(',')
        demand : int = 0

        for edge_info in split:
            if (edge_info == 'demand'):
                demand = getIntValueFromTitle(split, edge_info)

        org = Node(int(nodes[0]) - 1)
        dst = Node(int(nodes[1]) - 1)

        edge = Edge(
            len(graph.edges),
            org,
            dst,
            demand
        )

        org.addEdge(edge)
        # dst.addEdge(edge)

        graph.addNode(org)
        graph.addNode(dst)
        # graph.addEdge(edge)

def setDepotColors(graph):
    colors = ["#"+''.join([random.choice('0123456789ABCDEF') for _ in range(6)])
                    for _ in enumerate(graph.depots)]

    for i, c in enumerate(colors):
        graph.depots[i].color = c