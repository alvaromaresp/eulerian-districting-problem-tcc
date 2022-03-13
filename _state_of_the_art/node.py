from edge import Edge
from .._abstracts._node import _Node

class Node(_Node):
    def __init__(self):
        self.depot_parity : int = None
        self.incident_edges : list[Edge] = []

    def addIncidentEdge(self, edge : Edge):
        self.incident_edges.append(edge)

    def __str__(self):
        return (
            'Node: ' + str(self.id) + '\n' +
            '# of edges: ' + str(len(self.incident_edges)) + '\n')

    def printEdges(self):
        for e in self.incident_edges:
            print(e)