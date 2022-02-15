import random
from uuid import getnode
from graph import Graph
from edge import Edge
from node import Node

def processFile(file, graph : Graph) -> None:
    for line in file:
        split = line.split(' ')
        
        getNodeNumber(split, graph)

        getVehiclesNumber(split, graph)

        getCapacity(split, graph)

        getEdge(split, graph)

    graph.addDepot(0)
    graph.addDepot(1)
    graph.addDepot(2)
    
    colors = ["#"+''.join([random.choice('0123456789ABCDEF') for _ in range(6)])
                    for _ in enumerate(graph.depots)]

    graph.setDepotColors(colors)
    graph.setNodeDegree()
    graph.setNodeParity()
    graph.setAllShortestPaths()

def getNodeNumber(split, graph):
    if (split[0] == "NODES"):
        n_nodes = split[2].replace('\n','')
        graph.setN_Nodes(int(n_nodes))

def getVehiclesNumber(split, graph):
    if (split[0] == "VEHICLES"):
            vehicles = split[2].replace('\n', '')
            graph.setVehicles(int(vehicles))

def getCapacity(split, graph):
    if (split[0] == "VEHICLES"):
        vehicles = split[2].replace('\n', '')
        graph.setVehicles(int(vehicles))

def getEdge(split, graph):
    if (split[0][0] == '('):
        nodes = split[0][1:-1].split(',')
        cost : int = None
        demand : int = 0

        for edge_info in split:
            if (edge_info == 'trav_cost' or edge_info == 'cost'):
                cost = getIntValueFromTitle(split, edge_info)
            if (edge_info == 'demand'):
                demand = getIntValueFromTitle(split, edge_info)
        
        org = Node(int(nodes[0]) - 1)
        dst = Node(int(nodes[1]) - 1)

        edge = Edge(
            len(graph.edges),
            int(nodes[0]),
            int(nodes[1]),
            cost,
            demand
        )

        #Are we considering arcs?
        org.addIncidentEdge(edge)
        dst.addIncidentEdge(edge)

        graph.addNode(org)
        graph.addNode(dst)
        graph.addEdge(edge)

def getIntValueFromTitle(line : list[str], title : str) -> int:
    value_index = line.index(title) + 1
    value = line[value_index]
    try :
        value = value.replace('\n', '')
        return int(value)
    except:
        return int(value)


