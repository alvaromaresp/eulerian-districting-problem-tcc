import random
import time
from edge import Edge
from node import Node
from graph import Graph

def processFile(file, graph: Graph, num_depots: int, weightless: bool = False) -> None:

    for line in file:
        processLine(line, graph, weightless)

    for _ in range(num_depots):
        node = random.choice(graph.nodes)

        while node.id in list(map(lambda n: n.initial_node.id, graph.depots)):
                node = random.choice(graph.nodes)

        graph.addDepot(node)           

    # graph.addDepot(graph.getNodeById(68))
    # graph.addDepot(graph.getNodeById(69))
    # graph.addDepot(graph.getNodeById(70))
    # graph.addDepot(graph.getNodeById(graph.num_nodes - 1))

    setDepotColors(graph)
    
    graph.prepareData()

def processLine(line : str, graph: Graph, weightless: bool):
    split = line.split(' ')

    getNodeNumber(split, graph)

    buildEdgeFromLine(split, graph, weightless)


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

def buildEdgeFromLine(split: str, graph : Graph, weightless: bool):
    if (split[0][0] == '('):
        nodes = split[0][1:-1].split(',')
        demand : int = 0
        weight : int = 1 if weightless else 0

        for edge_info in split:
            if (edge_info == 'demand'):
                demand = getIntValueFromTitle(split, edge_info)

            if (not weightless):
                if (edge_info == 'serv_cost' or (weight == 0 and edge_info == 'cost')):
                    weight = getIntValueFromTitle(split, edge_info)


        org = Node(int(nodes[0]))
        dst = Node(int(nodes[1]))

        if (demand > graph.highestDemand):
            graph.highestDemand = demand

        edge = Edge(
            len(graph.edges),
            org,
            dst,
            demand,
            weight
        )

        # print("Weight: " + str(weight))
        # time.sleep(2)

        # org.addEdge(edge)
        # dst.addEdge(edge)

        # graph.addNode(org)
        # graph.addNode(dst)
        graph.addEdge(edge)

def setDepotColors(graph):
    colors = ["#"+''.join([random.choice('0123456789ABCDEF') for _ in range(6)])
                    for _ in enumerate(graph.depots)]

    for i, c in enumerate(colors):
        graph.depots[i].color = c