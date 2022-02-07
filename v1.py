import sys

from graph import Graph
from edge import Edge

from data_processing import *


file = None

if (len(sys.argv) > 1):
    file = open(sys.argv[1])
else:
    exit()

graph = Graph()

processFile(file, graph)


