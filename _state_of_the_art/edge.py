class Edge():

    def __init__(self, id: int, org : int, dst : int, demand : int):
        self.id: int = id
        self.org : int = org
        self.dst : int = dst
        self.demand : int = demand
        self.depot_id : int = -1

    def __str__(self):
        return '(' + str(self.org.id) + ',' + str(self.dst.id) + ') - DISTRICT: ' + str(self.depot_id)
