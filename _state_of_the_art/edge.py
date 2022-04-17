class Edge():

    def __init__(self, id: int, org : int, dst : int, demand : int):
        self.id: int = id
        self.org : int = org
        self.dst : int = dst
        self.demand : int = demand

    def __str__(self):
        return '(' + str(self.org) + ',' + str(self.dst) + ')'
