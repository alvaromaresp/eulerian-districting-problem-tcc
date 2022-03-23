class Edge():

    def __init__(self, id, org, dst, demand : int):
        self.id: int = id
        self.org = org
        self.dst = dst
        self.demand : int = demand
        self.depot_id : int = -1

    def __str__(self):
        return (
            'N1: ' + str(self.org.id) + '\n' +
            'N2: ' + str(self.dst.id) + '\n' +
            'demand: ' + str(self.demand))
