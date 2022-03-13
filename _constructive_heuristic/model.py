import sys

from graph import Graph
from .._abstracts._edge import Edge

from .._abstracts._data_processing import *
from .._abstracts._model import _Model

class ConstructiveModel(_Model):

    def execute(self, graph : Graph):
        
        for depot in graph.depots:
            depot.


    