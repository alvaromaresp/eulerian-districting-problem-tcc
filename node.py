from edge import Edge

class Node:
    def __init__(self, id):
        self.id : int = id
        self.incident_edges : list[Edge] = []
        self.depot_parity : int = None
        self.degree : int = None
    
    def addIncidentEdge(self, edge):
        self.incident_edges.append(edge)

    def __str__(self):
        return (
            'Node: ' + str(self.id) + '\n' +
            '# of edges: ' + str(len(self.incident_edges)) + '\n' +
            'degree: ' + str(self.degree) + '\n')

    def printEdges(self):
        for e in self.incident_edges:
            print(e)