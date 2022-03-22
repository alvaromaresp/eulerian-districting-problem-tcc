class _Edge:

    def __init__(self, id: int, org : int, dst : int, cost : int, demand : int):
        self.id: int = id
        self.cost : int = cost
        self.demand : int = demand
        self.depot_id : int = -1

    def __str__(self):
        return (
            'N1: ' + str(self.org) + '\n' +
            'N2: ' + str(self.dst) + '\n' +
            'cost: ' + str(self.cost) + '\n'
            'demand: ' + str(self.demand))
