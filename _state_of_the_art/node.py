from edge import Edge

class Node():
    def __init__(self, id):
        self.id : int = id
        self.edges : list[Edge] = []
        self.degree : int = 0

    def addEdge(self, edge : Edge):
        self.edges.append(edge)
        self.degree = self.degree + 1

    def __str__(self):
        self.printEdges()
        return (
            'Node: ' + str(self.id) + '\n' +
            '# of edges: ' + str(len(self.edges)) + '\n' +
            'Degree: ' + str(self.degree) + '\n')

    def printEdges(self):
        for e in self.edges:
            print(e)