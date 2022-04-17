class Edge():

    def __init__(self, id, org, dst, demand : int, weight : int):
        self.id: int = id
        self.org = org
        self.dst = dst
        self.demand : int = demand
        self.depot_id : int = -1
        self.weight : int = weight

    def __str__(self):
        return '(' + str(self.org.id) + ',' + str(self.dst.id) + ') - DISTRICT: ' + str(self.depot_id)

    def previewNodesParityInDistrict(self, depot_id : int):
        return self.org.previewNodeParityInDistrict(depot_id) + self.dst.previewNodeParityInDistrict(depot_id)
