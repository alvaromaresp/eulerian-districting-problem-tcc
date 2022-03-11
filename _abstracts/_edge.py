class _Edge:

    def __init__(self, id: int, org : int, dst : int, cost : int, demand : int):
        self.id: int = id
        self.org : int = org
        self.dst : int = dst
        self.cost : int = cost
        self.demand : int = demand

    def __str__(self):
        return (
            'N1: ' + str(self.org) + '\n' +
            'N2: ' + str(self.dst) + '\n' +
            'cost: ' + str(self.cost) + '\n'
            'demand: ' + str(self.demand))
