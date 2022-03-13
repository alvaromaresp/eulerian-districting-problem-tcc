from .._abstracts._edge import _Edge

class Edge(_Edge):

    def __init__(self, int, org : int, dst : int):
        self.org : int = org
        self.dst : int = dst

    def __str__(self):
        return (
            'N1: ' + str(self.org) + '\n' +
            'N2: ' + str(self.dst) + '\n' +
            'cost: ' + str(self.cost) + '\n'
            'demand: ' + str(self.demand))
