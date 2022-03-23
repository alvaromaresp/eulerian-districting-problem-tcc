import sys
from model import ConstructiveModel
from data_processing import processFile
from graph import Graph

def main():
    file = None

    if (len(sys.argv) > 1):
        file = open(sys.argv[1])
    else:
        exit()

    graph = Graph()

    processFile(file, graph, 4)

    model = ConstructiveModel()

    model.execute(graph)


if __name__ == "__main__":
    main()