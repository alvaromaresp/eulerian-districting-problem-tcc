from graph import Graph
from edge import Edge

def processFile(file, graph : Graph) -> None:
    for line in file:
        split = line.split(' ')
        
        if (split[0] == "NODES"):
            n_nodes = split[2].replace('\n','')
            graph.setN_Nodes(int(n_nodes))

        if (split[0] == "VEHICLES"):
            vehicles = split[2].replace('\n', '')
            graph.setVehicles(int(vehicles))
        
        if (split[0] == "CAPACITY"):
            capacity = split[2].replace('\n', '')
            graph.setCapacity(int(capacity))
        
        if (split[0][0] == '('):
            nodes = split[0][1:-1].split(',')
            cost : int = None
            demand : int = None

            for edge_info in split:
                if (edge_info == 'trav_cost' or edge_info == 'cost'):
                    cost = getIntValueFromTitle(split, edge_info)
                if (edge_info == 'demand'):
                    demand = getIntValueFromTitle(split, edge_info)
            
            graph.addEdge(Edge(
                int(nodes[0]),
                int(nodes[1]),
                cost,
                demand
            ))

            graph.setN_Nodes()
            graph.setNodeParity()

def getIntValueFromTitle(line : list[str], title : str) -> int:
    value_index = line.index(title) + 1
    value = line[value_index]
    try :
        value = value.replace('\n', '')
        return value
    except:
        return value

