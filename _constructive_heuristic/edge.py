class Edge():

    def __init__(self, id, org, dst, demand : int):
        self.id: int = id
        self.org = org
        self.dst = dst
        self.demand : int = demand
        self.depot_id : int = -1

    def __str__(self):
        return '(' + str(self.org.id) + ',' + str(self.dst.id) + ')'
