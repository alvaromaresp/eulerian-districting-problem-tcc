import sys
from .._abstracts._data_processing import DataProcessing
from graph import Graph

def main():
    file = None

    if (len(sys.argv) > 1):
        file = open(sys.argv[1])
    else:
        exit()

    graph = Graph()

    DataProcessing.processFile(file, graph)

if __name__ == "__main__":
    main()