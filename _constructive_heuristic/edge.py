from .._abstracts._edge import _Edge
from node import Node

class Edge(_Edge):

    def __init__(self, org : Node, dst : Node):
        self.org : Node = org
        self.dst : Node = dst

    def __str__(self):
        return (
            'N1: ' + str(self.org.id) + '\n' +
            'N2: ' + str(self.dst.id) + '\n' +
            'cost: ' + str(self.cost) + '\n'
            'demand: ' + str(self.demand))
