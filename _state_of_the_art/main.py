import sys
from _state_of_the_art.model import SOTA_Model

from data_processing import DataProcessing
from graph import Graph

def main():
    file = None

    if (len(sys.argv) > 1):
        file = open(sys.argv[1])
    else:
        exit()

    graph = Graph()

    DataProcessing.processFile(file, graph)

    model = SOTA_Model()

    model.execute(graph)

if __name__ == "__main__":
    main()