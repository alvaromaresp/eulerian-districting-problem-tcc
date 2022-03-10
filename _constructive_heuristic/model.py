import sys

from state_of_the_art.graph import Graph
from state_of_the_art.edge import Edge

from state_of_the_art.article_data_processing import *


file = None

if (len(sys.argv) > 1):
    file = open(sys.argv[1])
else:
    exit()

graph = Graph()

processFile(file, graph)


